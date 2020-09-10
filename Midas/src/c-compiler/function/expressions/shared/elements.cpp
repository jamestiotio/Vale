#include <iostream>

#include "translatetype.h"

#include "shared.h"
#include "branch.h"
#include "weaks.h"
#include "elements.h"
#include "utils/counters.h"

LLVMValueRef getKnownSizeArrayContentsPtr(
    LLVMBuilderRef builder,
    WrapperPtrLE knownSizeArrayWrapperPtrLE) {
  return LLVMBuildStructGEP(
      builder,
      knownSizeArrayWrapperPtrLE.refLE,
      1, // Array is after the control block.
      "ksaElemsPtr");
}

LLVMValueRef getUnknownSizeArrayContentsPtr(
    LLVMBuilderRef builder,
    WrapperPtrLE arrayWrapperPtrLE) {

  return LLVMBuildStructGEP(
      builder,
      arrayWrapperPtrLE.refLE,
      2, // Array is after the control block and length.
      "usaElemsPtr");
}

LLVMValueRef getUnknownSizeArrayLengthPtr(
    LLVMBuilderRef builder,
    WrapperPtrLE unknownSizeArrayWrapperPtrLE) {
  auto resultLE =
      LLVMBuildStructGEP(
          builder,
          unknownSizeArrayWrapperPtrLE.refLE,
          1, // Length is after the control block and before contents.
          "usaLenPtr");
  assert(LLVMTypeOf(resultLE) == LLVMPointerType(LLVMInt64Type(), 0));
  return resultLE;
}

WrapperPtrLE getKnownSizeArrayWrapperPtr(
    GlobalState* globalState,
    FunctionState* functionState,
    LLVMBuilderRef builder,
    Reference* ksaMT,
    Ref ksaRef) {
  switch (globalState->opt->regionOverride) {
    case RegionOverride::ASSIST:
    case RegionOverride::NAIVE_RC:
    case RegionOverride::FAST: {
      return WrapperPtrLE(ksaMT, checkValidReference(FL(), globalState, functionState, builder, ksaMT, ksaRef));
      break;
    }
    case RegionOverride::RESILIENT_V0:
    case RegionOverride::RESILIENT_V1:
    case RegionOverride::RESILIENT_V2: {
      switch (ksaMT->ownership) {
        case Ownership::SHARE:
        case Ownership::OWN:
          return WrapperPtrLE(ksaMT, checkValidReference(FL(), globalState, functionState, builder, ksaMT, ksaRef));
        case Ownership::BORROW:
          return lockWeakRef(FL(), globalState, functionState, builder, ksaMT, ksaRef);
        case Ownership::WEAK:
          assert(false); // VIR never loads from a weak ref
      }
      assert(false);
    }
    default:
      assert(false);
  }
}

WrapperPtrLE getUnknownSizeArrayWrapperPtr(
    GlobalState* globalState,
    FunctionState* functionState,
    LLVMBuilderRef builder,
    Reference* arrayRefMT,
    Ref arrayRef) {
  switch (globalState->opt->regionOverride) {
    case RegionOverride::ASSIST:
    case RegionOverride::NAIVE_RC:
    case RegionOverride::FAST: {
      return WrapperPtrLE(arrayRefMT, checkValidReference(FL(), globalState, functionState, builder, arrayRefMT, arrayRef));
    }
    case RegionOverride::RESILIENT_V0:
    case RegionOverride::RESILIENT_V1:
    case RegionOverride::RESILIENT_V2: {
      switch (arrayRefMT->ownership) {
        case Ownership::SHARE:
        case Ownership::OWN:
          return WrapperPtrLE(arrayRefMT, checkValidReference(FL(), globalState, functionState, builder, arrayRefMT, arrayRef));
        case Ownership::BORROW:
          return lockWeakRef(FL(), globalState, functionState, builder, arrayRefMT, arrayRef);
        case Ownership::WEAK:
          assert(false); // VIR never loads from a weak ref
      }
      break;
    }
    default:
      assert(false);
  }
  assert(false);
}

Ref getUnknownSizeArrayLength(
    GlobalState* globalState,
    FunctionState* functionState,
    LLVMBuilderRef builder,
    WrapperPtrLE arrayRefLE) {
  auto lengthPtrLE = getUnknownSizeArrayLengthPtr(builder, arrayRefLE);
  auto intLE = LLVMBuildLoad(builder, lengthPtrLE, "usaLen");
  return wrap(functionState->defaultRegion, globalState->metalCache.intRef, intLE);
}

Ref getUnknownSizeArrayLength(
    GlobalState* globalState,
    FunctionState* functionState,
    LLVMBuilderRef builder,
    Reference* arrayRefM,
    Ref arrayRef) {
  auto wrapperPtrLE = getUnknownSizeArrayWrapperPtr(globalState, functionState, builder, arrayRefM, arrayRef);
  return getUnknownSizeArrayLength(globalState, functionState, builder, wrapperPtrLE);
}

LLVMValueRef loadInnerArrayMember(
    GlobalState* globalState,
    LLVMBuilderRef builder,
    LLVMValueRef elemsPtrLE,
    Reference* elementRefM,
    LLVMValueRef indexLE) {
  assert(LLVMGetTypeKind(LLVMTypeOf(elemsPtrLE)) == LLVMPointerTypeKind);
  LLVMValueRef indices[2] = {
      constI64LE(0),
      indexLE
  };
  auto resultLE =
      LLVMBuildLoad(
          builder,
          LLVMBuildGEP(
              builder, elemsPtrLE, indices, 2, "indexPtr"),
          "index");

  return resultLE;
}

void storeInnerArrayMember(
    GlobalState* globalState,
    LLVMBuilderRef builder,
    LLVMValueRef elemsPtrLE,
    LLVMValueRef indexLE,
    LLVMValueRef sourceLE) {
  assert(LLVMGetTypeKind(LLVMTypeOf(elemsPtrLE)) == LLVMPointerTypeKind);
  LLVMValueRef indices[2] = {
      constI64LE(0),
      indexLE
  };
  LLVMBuildStore(
      builder,
      sourceLE,
      LLVMBuildGEP(
          builder, elemsPtrLE, indices, 2, "indexPtr"));

}

Ref loadElement(
    GlobalState* globalState,
    FunctionState* functionState,
    BlockState* blockState,
    LLVMBuilderRef builder,
    Reference* arrayRefM,
    Reference* elementRefM,
    Ref sizeRef,
    LLVMValueRef arrayPtrLE,
    Mutability mutability,
    Ref indexRef,
    Reference* resultRefM) {
  auto indexLE = checkValidReference(FL(), globalState, functionState, builder, globalState->metalCache.intRef, indexRef);
  auto sizeLE = checkValidReference(FL(), globalState, functionState, builder, globalState->metalCache.intRef, sizeRef);

  auto isNonNegativeLE = LLVMBuildICmp(builder, LLVMIntSGE, indexLE, constI64LE(0), "isNonNegative");
  auto isUnderLength = LLVMBuildICmp(builder, LLVMIntSLT, indexLE, sizeLE, "isUnderLength");
  auto isWithinBounds = LLVMBuildAnd(builder, isNonNegativeLE, isUnderLength, "isWithinBounds");
  buildFlare(FL(), globalState, functionState, builder, "index: ", indexLE);
  buildFlare(FL(), globalState, functionState, builder, "size: ", sizeLE);
  buildAssert(globalState, functionState, builder, isWithinBounds, "Index out of bounds!");

  LLVMValueRef fromArrayLE = nullptr;
  if (mutability == Mutability::IMMUTABLE) {
    if (arrayRefM->location == Location::INLINE) {
      assert(false);
//      return LLVMBuildExtractValue(builder, structExpr, indexLE, "index");
    } else {
      fromArrayLE = loadInnerArrayMember(globalState, builder, arrayPtrLE, elementRefM, indexLE);
    }
  } else if (mutability == Mutability::MUTABLE) {
    fromArrayLE = loadInnerArrayMember(globalState, builder, arrayPtrLE, elementRefM, indexLE);
  } else {
    assert(false);
  }
  return upgradeLoadResultToRefWithTargetOwnership(globalState, functionState, builder, elementRefM,
      resultRefM,
      fromArrayLE);
}


Ref storeElement(
    GlobalState* globalState,
    FunctionState* functionState,
    BlockState* blockState,
    LLVMBuilderRef builder,
    Reference* arrayRefM,
    Reference* elementRefM,
    Ref sizeRef,
    LLVMValueRef arrayPtrLE,
    Mutability mutability,
    Ref indexRef,
    Ref sourceRef) {
  auto sizeLE = checkValidReference(FL(), globalState, functionState, builder, globalState->metalCache.intRef, sizeRef);

  auto indexLE = checkValidReference(FL(), globalState, functionState, builder, globalState->metalCache.intRef, indexRef);
  auto isNonNegativeLE = LLVMBuildICmp(builder, LLVMIntSGE, indexLE, constI64LE(0), "isNonNegative");
  auto isUnderLength = LLVMBuildICmp(builder, LLVMIntSLT, indexLE, sizeLE, "isUnderLength");
  auto isWithinBounds = LLVMBuildAnd(builder, isNonNegativeLE, isUnderLength, "isWithinBounds");
  buildAssert(globalState, functionState, builder, isWithinBounds, "Index out of bounds!");

//  auto arrayPtrLE = checkValidReference(FL(), globalState, functionState, builder, arrayRefM, arrayRef);
  auto sourceLE = checkValidReference(FL(), globalState, functionState, builder, elementRefM, sourceRef);

  if (mutability == Mutability::IMMUTABLE) {
    if (arrayRefM->location == Location::INLINE) {
      assert(false);
//      return LLVMBuildExtractValue(builder, structExpr, indexLE, "index");
    } else {
      auto resultLE = loadInnerArrayMember(globalState, builder, arrayPtrLE, elementRefM, indexLE);
      storeInnerArrayMember(globalState, builder, arrayPtrLE, indexLE, sourceLE);
      return wrap(functionState->defaultRegion, elementRefM, resultLE);
    }
  } else if (mutability == Mutability::MUTABLE) {
    auto resultLE = loadInnerArrayMember(globalState, builder, arrayPtrLE, elementRefM, indexLE);
    storeInnerArrayMember(globalState, builder, arrayPtrLE, indexLE, sourceLE);
    return wrap(functionState->defaultRegion, elementRefM, resultLE);
  } else {
    assert(false);
  }
}


void foreachArrayElement(
    GlobalState* globalState,
    FunctionState* functionState,
    LLVMBuilderRef builder,
    Ref sizeRef,
    LLVMValueRef arrayPtrLE,
    std::function<void(Ref, LLVMBuilderRef)> iterationBuilder) {
  LLVMValueRef iterationIndexPtrLE =
      makeMidasLocal(
          functionState,
          builder,
          LLVMInt64Type(),
          "iterationIndex",
          LLVMConstInt(LLVMInt64Type(),0, false));

  auto sizeLE = checkValidReference(FL(), globalState, functionState, builder, globalState->metalCache.intRef, sizeRef);

  buildWhile(
      globalState,
      functionState,
      builder,
      [globalState, functionState, sizeLE, iterationIndexPtrLE](LLVMBuilderRef conditionBuilder) {
        auto iterationIndexLE =
            LLVMBuildLoad(conditionBuilder, iterationIndexPtrLE, "iterationIndex");
        auto isBeforeEndLE =
            LLVMBuildICmp(
                conditionBuilder,LLVMIntSLT,iterationIndexLE,sizeLE,"iterationIndexIsBeforeEnd");
        return wrap(functionState->defaultRegion, globalState->metalCache.boolRef, isBeforeEndLE);
      },
      [globalState, functionState, iterationBuilder, iterationIndexPtrLE, arrayPtrLE](LLVMBuilderRef bodyBuilder) {
        auto iterationIndexLE = LLVMBuildLoad(bodyBuilder, iterationIndexPtrLE, "iterationIndex");
        auto iterationIndexRef = wrap(functionState->defaultRegion, globalState->metalCache.intRef, iterationIndexLE);
        iterationBuilder(iterationIndexRef, bodyBuilder);
        adjustCounter(bodyBuilder, iterationIndexPtrLE, 1);
      });
}
