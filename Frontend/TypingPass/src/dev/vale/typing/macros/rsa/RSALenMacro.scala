package dev.vale.typing.macros.rsa

import dev.vale.{Keywords, RangeS, StrI, vimpl}
import dev.vale.highertyping.FunctionA
import dev.vale.postparsing.LocationInDenizen
import dev.vale.typing.CompilerOutputs
import dev.vale.typing.ast.{ArgLookupTE, ArrayLengthTE, BlockTE, FunctionDefinitionT, FunctionHeaderT, LocationInFunctionEnvironmentT, ParameterT, ReturnTE}
import dev.vale.typing.env.FunctionEnvironmentT
import dev.vale.typing.macros.IFunctionBodyMacro
import dev.vale.typing.types.CoordT
import dev.vale.typing.ast._
import dev.vale.typing.ast


class RSALenMacro(keywords: Keywords) extends IFunctionBodyMacro {
  val generatorId: StrI = keywords.vale_runtime_sized_array_len

  def generateFunctionBody(
    env: FunctionEnvironmentT,
    coutputs: CompilerOutputs,
    generatorId: StrI,
    life: LocationInFunctionEnvironmentT,
    callRange: List[RangeS],
      callLocation: LocationInDenizen,
    originFunction: Option[FunctionA],
    paramCoords: Vector[ParameterT],
    maybeRetCoord: Option[CoordT]):
  (FunctionHeaderT, ReferenceExpressionTE) = {
    val header =
      FunctionHeaderT(env.id, Vector.empty, paramCoords, maybeRetCoord.get, Some(env.templata))
    val body =
      BlockTE(
        ReturnTE(
          ArrayLengthTE(
            ArgLookupTE(0, paramCoords(0).tyype))))
    (header, body)
  }
}