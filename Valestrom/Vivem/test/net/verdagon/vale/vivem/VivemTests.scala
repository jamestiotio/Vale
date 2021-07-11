package net.verdagon.vale.vivem

import net.verdagon.vale.metal._
import net.verdagon.vale.{PackageCoordinate, PackageCoordinateMap, metal => m}
import net.verdagon.von.{VonArray, VonInt, VonMember, VonObject, VonStr}
import org.scalatest.{FunSuite, Matchers}

class VivemTests extends FunSuite with Matchers {
  test("Return 7") {
    val main =
      FunctionH(
        PrototypeH(
          FullNameH(
            "main",
            0,
            PackageCoordinate.TEST_TLD,
            List(VonObject("F",None,Vector(VonMember("humanName",VonStr("main")), VonMember("templateArgs",VonArray(None,Vector())), VonMember("parameters",VonArray(None,Vector())))))),List.empty,ReferenceH(m.ShareH,InlineH,ReadonlyH,IntH.i32)),
        true,
        false,
        List(UserFunctionH),
        BlockH(ConstantIntH(7, 32)))
    val programH =
      ProgramH(
        PackageCoordinateMap(Map())
          .add(PackageCoordinate.TEST_TLD, PackageH(List.empty, List.empty, List(main), List.empty, List.empty, Map(), Map("main" -> main.prototype), Map(), Map(), Map())))
    val result =
      Vivem.executeWithPrimitiveArgs(programH, Vector(), System.out, Vivem.emptyStdin, Vivem.nullStdout)
    result shouldEqual VonInt(7)
  }

  test("Adding") {
    val intRef =
      VonObject("Ref",None,Vector(VonMember("ownership",VonObject("Share",None,Vector())), VonMember("location",VonObject("Inline",None,Vector())), VonMember("permission",VonObject("Readonly",None,Vector())), VonMember("kind",VonObject("Int",None,Vector(VonMember("bits", VonInt(32)))))))

    val addPrototype =
      PrototypeH(
        FullNameH(
          "__addI32",
          0,
          PackageCoordinate.BUILTIN,
          List(VonObject("F",None,Vector(VonMember("humanName",VonStr("__addI32")), VonMember("templateArgs",VonArray(None,Vector())), VonMember("parameters",VonArray(None,Vector(intRef, intRef))))))),
        List(ReferenceH(ShareH,InlineH,ReadonlyH,IntH.i32), ReferenceH(ShareH,InlineH,ReadonlyH,IntH.i32)),
        ReferenceH(ShareH,InlineH,ReadonlyH,IntH.i32))
    val main =
      FunctionH(
        PrototypeH(
          FullNameH(
            "main",
            0,
            PackageCoordinate.TEST_TLD,
            List(VonObject("F",None,Vector(VonMember("humanName",VonStr("main")), VonMember("templateArgs",VonArray(None,Vector())), VonMember("parameters",VonArray(None,Vector())))))),List.empty,ReferenceH(m.ShareH,InlineH,ReadonlyH,IntH.i32)),
        true,
        false,
        List(UserFunctionH),
        BlockH(
          CallH(
            addPrototype,
            List(
              ConstantIntH(52, 32),
              CallH(
                addPrototype,
                List(
                  ConstantIntH(53, 32),
                  ConstantIntH(54, 32)))))))
    val addExtern =
      FunctionH(
        addPrototype,
        false,
        true,
        List.empty,
        BlockH(ConstantIntH(133337, 32)))
    val programH =
      ProgramH(
        PackageCoordinateMap(Map())
          .add(PackageCoordinate.BUILTIN, PackageH(List.empty, List.empty, List(addExtern), List.empty, List.empty, Map(), Map(), Map(), Map("__addI32" -> addPrototype), Map()))
          .add(PackageCoordinate.TEST_TLD, PackageH(List.empty, List.empty, List(main), List.empty, List.empty, Map(), Map("main" -> main.prototype), Map(), Map(), Map())))
    val result =
      Vivem.executeWithPrimitiveArgs(programH, Vector(), System.out, Vivem.emptyStdin, Vivem.nullStdout)
    result shouldEqual VonInt(159)
  }
}
