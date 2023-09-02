package dev.vale.typing.env

import dev.vale.highertyping.FunctionA
import dev.vale.{Interner, vassert, vcurious, vfail, vpass}
import dev.vale.postparsing._
import dev.vale.typing.ast.{LocationInFunctionEnvironmentT, ParameterT}
import dev.vale.typing.names._
import dev.vale.typing.templata._
import dev.vale.typing.types._
import dev.vale.highertyping._
import dev.vale.postparsing.IImpreciseNameS
import dev.vale.typing._
import dev.vale.typing.types.StructTT
import dev.vale.{Interner, Profiler, vassert, vcurious, vfail, vimpl, vpass, vwat}

import scala.collection.immutable.{List, Map, Set}

case class BuildingFunctionEnvironmentWithClosuredsT(
  globalEnv: GlobalEnvironment,
  parentEnv: IEnvironmentT,
  id: IdT[IFunctionTemplateNameT],
//  defaultRegion: ITemplata[RegionTemplataType],
  templatas: TemplatasStore,
  function: FunctionA,
  variables: Vector[IVariableT],
  isRootCompilingDenizen: Boolean
) extends IInDenizenEnvironmentT {

  def templata = FunctionTemplataT(parentEnv, function)

  override def denizenTemplateId: IdT[ITemplateNameT] = id

  override def currentHeight: Int = 0

  override def pureHeight: Option[Int] = {
    if (function.attributes.exists({ case PureS => true case _ => false})) {
      Some(0)
    } else {
      None
    }
  }

  override def additiveHeight: Option[Int] = {
    if (function.attributes.exists({ case AdditiveS => true case _ => false})) {
      Some(0)
    } else {
      None
    }
  }

  override def denizenId: IdT[INameT] = id

  val hash = runtime.ScalaRunTime._hashCode(id); override def hashCode(): Int = hash;
  override def equals(obj: Any): Boolean = {
    if (!obj.isInstanceOf[IInDenizenEnvironmentT]) {
      return false
    }
    return id.equals(obj.asInstanceOf[IInDenizenEnvironmentT].id)
  }

  override def rootCompilingDenizenEnv: IInDenizenEnvironmentT = {
    if (isRootCompilingDenizen) {
      this
    } else {
      parentEnv match {
        case PackageEnvironmentT(_, _, _) => vwat()
        case _ => {
          parentEnv match {
            case parentInDenizenEnv : IInDenizenEnvironmentT => {
              parentInDenizenEnv.rootCompilingDenizenEnv
            }
            case _ => vwat()
          }
        }
      }
    }
  }

  private[env] override def lookupWithNameInner(

    name: INameT,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithNameInner(
      this, templatas, parentEnv, name, lookupFilter, getOnlyNearest)
  }

  private[env] override def lookupWithImpreciseNameInner(

    name: IImpreciseNameS,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithImpreciseNameInner(
      this, templatas, parentEnv, name, lookupFilter, getOnlyNearest)
  }
}

case class BuildingFunctionEnvironmentWithClosuredsAndTemplateArgsT(
  globalEnv: GlobalEnvironment,
  parentEnv: IEnvironmentT,
  id: IdT[IFunctionTemplateNameT],
  templateArgs: Vector[ITemplataT[ITemplataType]],
  templatas: TemplatasStore,
  function: FunctionA,
  variables: Vector[IVariableT],
  isRootCompilingDenizen: Boolean,
  defaultRegion: RegionT
) extends IInDenizenEnvironmentT {

  override def currentHeight: Int = 0

  override def pureHeight: Option[Int] = {
    if (function.attributes.exists({ case PureS => true case _ => false})) {
      Some(0)
    } else {
      None
    }
  }

  override def additiveHeight: Option[Int] = {
    if (function.attributes.exists({ case AdditiveS => true case _ => false})) {
      Some(0)
    } else {
      None
    }
  }

  override def denizenTemplateId: IdT[ITemplateNameT] = id
  override def denizenId: IdT[INameT] = id

  val hash = runtime.ScalaRunTime._hashCode(id); override def hashCode(): Int = hash;
  override def equals(obj: Any): Boolean = {
    if (!obj.isInstanceOf[IInDenizenEnvironmentT]) {
      return false
    }
    return id.equals(obj.asInstanceOf[IInDenizenEnvironmentT].id)
  }

  override def rootCompilingDenizenEnv: IInDenizenEnvironmentT = {
    if (isRootCompilingDenizen) {
      this
    } else {
      parentEnv match {
        case PackageEnvironmentT(_, _, _) => vwat()
        case _ => {
          parentEnv match {
            case parentInDenizenEnv : IInDenizenEnvironmentT => {
              parentInDenizenEnv.rootCompilingDenizenEnv
            }
            case _ => vwat()
          }
        }
      }
    }
  }

  private[env] override def lookupWithNameInner(

    name: INameT,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithNameInner(
      this, templatas, parentEnv, name, lookupFilter, getOnlyNearest)
  }

  private[env] override def lookupWithImpreciseNameInner(

    name: IImpreciseNameS,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithImpreciseNameInner(
      this, templatas, parentEnv, name, lookupFilter, getOnlyNearest)
  }

}

case class NodeEnvironmentT(
  parentFunctionEnv: FunctionEnvironmentT,
  parentNodeEnv: Option[NodeEnvironmentT],
  node: IExpressionSE,
  life: LocationInFunctionEnvironmentT,

  // The things below are the "state"; they can be different for any given line in a function.
  templatas: TemplatasStore,
  // This contains locals from parent blocks, see WTHPFE.
  declaredLocals: Vector[IVariableT],
  // This can refer to vars in parent blocks, see UCRTVPE.
  unstackifiedLocals: Set[IVarNameT],
  // This can refer to vars in parent blocks, see UCRTVPE.
  restackifiedLocals: Set[IVarNameT],

  defaultRegion: RegionT,

  currentHeight: Int,
  // The location-in-denizen of the nearest enclosing pure block, if there is one. Otherwise, None.
  // This is used to know whether a region is currently mutable or immutable.
  pureHeight: Option[Int],
  additiveHeight: Option[Int],
) extends IInDenizenEnvironmentT {
  vassert(declaredLocals.map(_.name) == declaredLocals.map(_.name).distinct)

  val hash = id.hashCode() ^ life.hashCode();
  override def hashCode(): Int = hash;
  override def equals(obj: Any): Boolean = {
    obj match {
      case that @ NodeEnvironmentT(_, _, _, _, _, _, _, _, _, _, _, _) => {
        id == that.id && life == that.life
      }
    }
  }

  override def denizenTemplateId: IdT[ITemplateNameT] = parentFunctionEnv.denizenTemplateId
  override def denizenId: IdT[INameT] = parentFunctionEnv.denizenId

  override def rootCompilingDenizenEnv: IInDenizenEnvironmentT = {
//    parentEnv match {
//      case PackageEnvironment(_, _, _) => this
//      case _ => parentEnv.rootCompilingDenizenEnv
//    }
    parentEnv.rootCompilingDenizenEnv
  }

  override def id: IdT[IFunctionNameT] = parentFunctionEnv.id
  def function = parentFunctionEnv.function

  private[env] override def lookupWithNameInner(

    name: INameT,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithNameInner(
      this, templatas, parentNodeEnv.getOrElse(parentFunctionEnv), name, lookupFilter, getOnlyNearest)
  }

  private[env] override def lookupWithImpreciseNameInner(

    name: IImpreciseNameS,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithImpreciseNameInner(
      this, templatas, parentNodeEnv.getOrElse(parentFunctionEnv), name, lookupFilter, getOnlyNearest)
  }

  def globalEnv: GlobalEnvironment = parentFunctionEnv.globalEnv

  def parentEnv: IInDenizenEnvironmentT = {
    parentNodeEnv.getOrElse(parentFunctionEnv)
  }

  def getVariable(name: IVarNameT): Option[IVariableT] = {
    declaredLocals.find(_.name == name) match {
      case Some(v) => Some(v)
      case None => {
        parentNodeEnv match {
          case Some(p) => p.getVariable(name)
          case None => {
            parentFunctionEnv.closuredLocals.find(_.name == name)
          }
        }
      }
    }
  }

  // Dont have a getAllUnstackifiedLocals or getAllLiveLocals here. We learned that the hard way.
  // See UCRTVPE, child environments would be the ones that know about their unstackifying of locals
  // from parent envs.

  def getAllLocals(): Vector[ILocalVariableT] = {
    declaredLocals.collect({ case i : ILocalVariableT => i })
  }

  def getAllUnstackifiedLocals(): Vector[IVarNameT] = {
    unstackifiedLocals.toVector
  }

  def addVariables(newVars: Vector[IVariableT]): NodeEnvironmentT = {
    NodeEnvironmentT(
      parentFunctionEnv,
      parentNodeEnv,
      node,
      life,
      templatas,
      declaredLocals ++ newVars,
      unstackifiedLocals,
      restackifiedLocals,
      defaultRegion,
      currentHeight,
      pureHeight,
      additiveHeight)
  }
  def addVariable(newVar: IVariableT): NodeEnvironmentT = {
    NodeEnvironmentT(
      parentFunctionEnv,
      parentNodeEnv,
      node,
      life,
      templatas,
      declaredLocals :+ newVar,
      unstackifiedLocals,
      restackifiedLocals,
      defaultRegion,
      currentHeight,
      pureHeight,
      additiveHeight)
  }

  def getAllRestackifiedLocals(): Vector[IVarNameT] = {
    restackifiedLocals.toVector
  }

  def markLocalUnstackified(newUnstackified: IVarNameT): NodeEnvironmentT = {
    vassert(getAllLocals().exists(_.name == newUnstackified))
    vassert(!getAllUnstackifiedLocals().contains(newUnstackified))

    if (getAllRestackifiedLocals().contains(newUnstackified)) {
      // It was a restackified local, so don't mark it as unstackified, just undo the
      // restackification.
      // Even if the local belongs to a parent env, we still mark it unstackified here, see UCRTVPE.
      NodeEnvironmentT(
        parentFunctionEnv,
        parentNodeEnv,
        node,
        life,
        templatas,
        declaredLocals,
        unstackifiedLocals,
        restackifiedLocals - newUnstackified,
        defaultRegion,
        currentHeight,
        pureHeight,
        additiveHeight)
    } else {
      // Even if the local belongs to a parent env, we still mark it unstackified here, see UCRTVPE.
      NodeEnvironmentT(
        parentFunctionEnv,
        parentNodeEnv,
        node,
        life,
        templatas,
        declaredLocals,
        unstackifiedLocals + newUnstackified,
        restackifiedLocals,
        defaultRegion,
        currentHeight,
        pureHeight,
        additiveHeight)
    }
  }

  def markLocalRestackified(newRestackified: IVarNameT): NodeEnvironmentT = {
    vassert(getAllLocals().exists(_.name == newRestackified))
    vassert(!getAllRestackifiedLocals().contains(newRestackified))
    if (getAllUnstackifiedLocals().contains(newRestackified)) {
      // It was an unstackified local, so don't mark it as restackified, just undo the
      // unstackification.
      // Even if the local belongs to a parent env, we still mark it restackified here, see UCRTVPE.
      NodeEnvironmentT(
        parentFunctionEnv,
        parentNodeEnv,
        node,
        life,
        templatas,
        declaredLocals,
        unstackifiedLocals - newRestackified,
        restackifiedLocals,
        defaultRegion,
        currentHeight,
        pureHeight,
        additiveHeight)
    } else {
      // Even if the local belongs to a parent env, we still mark it restackified here, see UCRTVPE.
      NodeEnvironmentT(
        parentFunctionEnv,
        parentNodeEnv,
        node,
        life,
        templatas,
        declaredLocals,
        unstackifiedLocals,
        restackifiedLocals + newRestackified,
        defaultRegion,
        currentHeight,
        pureHeight,
        additiveHeight)
    }
  }

  // Gets the effects that this environment had on the outside world (on its parent
  // environments). In other words, parent locals that were unstackified.
  def getEffectsSince(earlierNodeEnv: NodeEnvironmentT): (Set[IVarNameT], Set[IVarNameT]) = {
    vassert(parentFunctionEnv == earlierNodeEnv.parentFunctionEnv)

    // We may have unstackified outside locals from inside the block, make sure
    // the parent environment knows about that.

    // declaredLocals contains things from parent environment, which is why we need to receive
    // an earlier environment to compare to, see WTHPFE.
    val earlierNodeEnvDeclaredLocals = earlierNodeEnv.declaredLocals.map(_.name).toSet
    val earlierNodeEnvLiveLocals = earlierNodeEnvDeclaredLocals -- earlierNodeEnv.unstackifiedLocals
    val liveLocalsIntroducedSinceEarlier =
      declaredLocals.map(_.name).filter(x => !earlierNodeEnvLiveLocals.contains(x))

    val unstackifiedAncestorLocals = unstackifiedLocals -- liveLocalsIntroducedSinceEarlier

    val restackifiedAncestorLocals = restackifiedLocals -- liveLocalsIntroducedSinceEarlier

    (unstackifiedAncestorLocals, restackifiedAncestorLocals)
  }

  def getLiveVariablesIntroducedSince(
    sinceNenv: NodeEnvironmentT):
  Vector[ILocalVariableT] = {
    val localsAsOfThen =
      sinceNenv.declaredLocals.collect({
        case x @ ReferenceLocalVariableT(_, _, _) => x
        case x @ AddressibleLocalVariableT(_, _, _) => x
      })
    val localsAsOfNow =
      declaredLocals.collect({
        case x @ ReferenceLocalVariableT(_, _, _) => x
        case x @ AddressibleLocalVariableT(_, _, _) => x
      })

    vassert(localsAsOfNow.startsWith(localsAsOfThen))
    val localsDeclaredSinceThen = localsAsOfNow.slice(localsAsOfThen.size, localsAsOfNow.size)
    vassert(localsDeclaredSinceThen.size == localsAsOfNow.size - localsAsOfThen.size)

    val unmovedLocalsDeclaredSinceThen =
      localsDeclaredSinceThen.filter(x => !unstackifiedLocals.contains(x.name))

    unmovedLocalsDeclaredSinceThen
  }

  def makeChild(
    node: IExpressionSE,
    maybeNewDefaultRegion: Option[RegionT],
    maybeNewHeight: Option[Int],
    maybeNewPureHeight: Option[Option[Int]],
    maybeNewAdditiveHeight: Option[Option[Int]]):
  NodeEnvironmentT = {
    NodeEnvironmentT(
      parentFunctionEnv,
      Some(this),
      node,
      life,
      TemplatasStore(id, Map(), Map()),
      declaredLocals, // See WTHPFE.
      unstackifiedLocals, // See WTHPFE
      restackifiedLocals, // See WTHPFE.
      maybeNewDefaultRegion.getOrElse(defaultRegion),
      // DO NOT SUBMIT cant we just do +1 here since it's a child?
      maybeNewHeight.getOrElse(currentHeight),
      maybeNewPureHeight.getOrElse(pureHeight),
      maybeNewAdditiveHeight.getOrElse(additiveHeight))
  }

  def addEntry(interner: Interner, name: INameT, entry: IEnvEntry): NodeEnvironmentT = {
    NodeEnvironmentT(
      parentFunctionEnv,
      parentNodeEnv,
      node,
      life,
      templatas.addEntry(interner, name, entry),
      declaredLocals,
      unstackifiedLocals,
      restackifiedLocals,
      defaultRegion,
      currentHeight,
      pureHeight,
      additiveHeight)
  }
  def addEntries(interner: Interner, newEntries: Vector[(INameT, IEnvEntry)]): NodeEnvironmentT = {
    NodeEnvironmentT(
      parentFunctionEnv,
      parentNodeEnv,
      node,
      life,
      templatas.addEntries(interner, newEntries),
      declaredLocals,
      unstackifiedLocals,
      restackifiedLocals,
      defaultRegion,
      currentHeight,
      pureHeight,
      additiveHeight)
  }

  def nearestBlockEnv(): Option[(NodeEnvironmentT, BlockSE)] = {
    node match {
      case b @ BlockSE(_, _, _) => Some((this, b))
      case _ => parentNodeEnv.flatMap(_.nearestBlockEnv())
    }
  }
  def nearestLoopEnv(): Option[(NodeEnvironmentT, IExpressionSE)] = {
    node match {
      case w @ WhileSE(_, _) => Some((this, w))
      case w @ MapSE(_, _) => Some((this, w))
      case _ => parentNodeEnv.flatMap(_.nearestLoopEnv())
    }
  }
}

case class NodeEnvironmentBox(var nodeEnvironment: NodeEnvironmentT) {
  override def equals(obj: Any): Boolean = vcurious(); override def hashCode(): Int = vfail() // Shouldnt hash, is mutable

  def snapshot: NodeEnvironmentT = nodeEnvironment
  def defaultRegion: RegionT = nodeEnvironment.defaultRegion
  def id: IdT[IFunctionNameT] = nodeEnvironment.parentFunctionEnv.id
  def node: IExpressionSE = nodeEnvironment.node
  def maybeReturnType: Option[CoordT] = nodeEnvironment.parentFunctionEnv.maybeReturnType
  def globalEnv: GlobalEnvironment = nodeEnvironment.globalEnv
  def declaredLocals: Vector[IVariableT] = nodeEnvironment.declaredLocals
  def unstackifieds: Set[IVarNameT] = nodeEnvironment.unstackifiedLocals
  def function = nodeEnvironment.function
  def functionEnvironment = nodeEnvironment.parentFunctionEnv

  def addVariable(newVar: IVariableT): Unit= {
    nodeEnvironment = nodeEnvironment.addVariable(newVar)
  }
  def markLocalUnstackified(newMoved: IVarNameT): Unit= {
    nodeEnvironment = nodeEnvironment.markLocalUnstackified(newMoved)
  }

  def markLocalRestackified(newMoved: IVarNameT): Unit= {
    nodeEnvironment = nodeEnvironment.markLocalRestackified(newMoved)
  }

  def getVariable(name: IVarNameT): Option[IVariableT] = {
    nodeEnvironment.getVariable(name)
  }

  def getAllLocals(): Vector[ILocalVariableT] = {
    nodeEnvironment.getAllLocals()
  }

  def getAllUnstackifiedLocals(): Vector[IVarNameT] = {
    nodeEnvironment.getAllUnstackifiedLocals()
  }

  def lookupNearestWithImpreciseName(

    nameS: IImpreciseNameS,
    lookupFilter: Set[ILookupContext]):
  Option[ITemplataT[ITemplataType]] = {
    nodeEnvironment.lookupNearestWithImpreciseName(nameS, lookupFilter)
  }

  def lookupNearestWithName(

    nameS: INameT,
    lookupFilter: Set[ILookupContext]):
  Option[ITemplataT[ITemplataType]] = {
    nodeEnvironment.lookupNearestWithName(nameS, lookupFilter)
  }

  def lookupAllWithImpreciseName( nameS: IImpreciseNameS, lookupFilter: Set[ILookupContext]): Array[ITemplataT[ITemplataType]] = {
    nodeEnvironment.lookupAllWithImpreciseName(nameS, lookupFilter)
  }

  def lookupAllWithName( nameS: INameT, lookupFilter: Set[ILookupContext]): Iterable[ITemplataT[ITemplataType]] = {
    nodeEnvironment.lookupAllWithName(nameS, lookupFilter)
  }

  private[env] def lookupWithImpreciseNameInner( nameS: IImpreciseNameS, lookupFilter: Set[ILookupContext], getOnlyNearest: Boolean) = {
    nodeEnvironment.lookupWithImpreciseNameInner(nameS, lookupFilter, getOnlyNearest)
  }

  private[env] def lookupWithNameInner( nameS: INameT, lookupFilter: Set[ILookupContext], getOnlyNearest: Boolean) = {
    nodeEnvironment.lookupWithNameInner(nameS, lookupFilter, getOnlyNearest)
  }

  def makeChild(
    node: IExpressionSE,
    maybeNewDefaultRegion: Option[RegionT],
    maybeNewHeight: Option[Int],
    maybeNewPureHeight: Option[Option[Int]],
    maybeNewAdditiveHeight: Option[Option[Int]]):
  NodeEnvironmentT = {
    nodeEnvironment.makeChild(
      node, maybeNewDefaultRegion, maybeNewHeight, maybeNewPureHeight, maybeNewAdditiveHeight)
  }

  def addEntry(interner: Interner, name: INameT, entry: IEnvEntry): Unit = {
    nodeEnvironment = nodeEnvironment.addEntry(interner, name, entry)
  }
  def addEntries(interner: Interner, newEntries: Vector[(INameT, IEnvEntry)]): Unit= {
    nodeEnvironment = nodeEnvironment.addEntries(interner, newEntries)
  }

  def nearestBlockEnv(): Option[(NodeEnvironmentT, BlockSE)] = {
    nodeEnvironment.nearestBlockEnv()
  }
  def nearestLoopEnv(): Option[(NodeEnvironmentT, IExpressionSE)] = {
    nodeEnvironment.nearestLoopEnv()
  }
}

case class FunctionEnvironmentT(
  // These things are the "environment"; they are the same for every line in a function.
  globalEnv: GlobalEnvironment,
  // This points to the environment containing the function, not parent blocks, see WTHPFE.
  parentEnv: IEnvironmentT,
  templateId: IdT[IFunctionTemplateNameT],
  id: IdT[IFunctionNameT], // Includes the name of the function

  templatas: TemplatasStore,

  function: FunctionA,
  maybeReturnType: Option[CoordT],

  closuredLocals: Vector[IVariableT],

  isRootCompilingDenizen: Boolean,

  defaultRegion: RegionT,

  // Eventually we might have a list of imported environments here, pointing at the
  // environments in the global environment.
) extends IInDenizenEnvironmentT {
  val hash = runtime.ScalaRunTime._hashCode(id); override def hashCode(): Int = hash;

  override def currentHeight: Int = 0

  override def pureHeight: Option[Int] = {
    if (function.attributes.exists({ case PureS => true case _ => false})) {
      Some(0)
    } else {
      None
    }
  }

  override def additiveHeight: Option[Int] = {
    if (function.attributes.exists({ case AdditiveS => true case _ => false})) {
      Some(0)
    } else {
      None
    }
  }

  override def denizenTemplateId: IdT[ITemplateNameT] = templateId
  override def denizenId: IdT[INameT] = templateId

  override def equals(obj: Any): Boolean = {
    if (!obj.isInstanceOf[IInDenizenEnvironmentT]) {
      return false
    }
    return id.equals(obj.asInstanceOf[IInDenizenEnvironmentT].id)
  }

  override def rootCompilingDenizenEnv: IInDenizenEnvironmentT = {
    if (isRootCompilingDenizen) {
      this
    } else {
      parentEnv match {
        case PackageEnvironmentT(_, _, _) => vwat()
        case _ => {
          parentEnv match {
            case parentInDenizenEnv : IInDenizenEnvironmentT => {
              parentInDenizenEnv.rootCompilingDenizenEnv
            }
            case _ => vwat()
          }
        }
      }
    }
  }

  def templata = FunctionTemplataT(parentEnv, function)

  def addEntry(interner: Interner, name: INameT, entry: IEnvEntry): FunctionEnvironmentT = {
    FunctionEnvironmentT(
      globalEnv,
      parentEnv,
      templateId,
      id,
      templatas.addEntry(interner, name, entry),
      function,
      maybeReturnType,
      closuredLocals,
      isRootCompilingDenizen,
      defaultRegion)
  }
  def addEntries(interner: Interner, newEntries: Vector[(INameT, IEnvEntry)]): FunctionEnvironmentT = {
    FunctionEnvironmentT(
      globalEnv,
      parentEnv,
      templateId,
      id,
      templatas.addEntries(interner, newEntries),
      function,
      maybeReturnType,
      closuredLocals,
      isRootCompilingDenizen,
      defaultRegion)
  }

  private[env] override def lookupWithNameInner(

    name: INameT,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithNameInner(
      this, templatas, parentEnv, name, lookupFilter, getOnlyNearest)
  }

  private[env] override def lookupWithImpreciseNameInner(
    name: IImpreciseNameS,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    EnvironmentHelper.lookupWithImpreciseNameInner(
      this, templatas, parentEnv, name, lookupFilter, getOnlyNearest)
  }

  def makeChildNodeEnvironment(node: IExpressionSE, life: LocationInFunctionEnvironmentT): NodeEnvironmentT = {
    // See WTHPFE, if this is a lambda, we let our blocks start with
    // locals from the parent function.
    val (declaredLocals, unstackifiedLocals, restackifiedLocals) =
      parentEnv match {
        case NodeEnvironmentT(_, _, _, _, _, declaredLocals, unstackifiedLocals, restackifiedLocals, _, _, _, _) => {
          (declaredLocals, unstackifiedLocals, restackifiedLocals)
        }
        case _ => (Vector(), Set[IVarNameT](), Set[IVarNameT]())
      }

    val currentHeight = 0
    val pureHeight = None
    val additiveHeight = None

    NodeEnvironmentT(
      this,
      None,
      node,
      life,
      TemplatasStore(id, Map(), Map()),
      declaredLocals, // See WTHPFE.
      unstackifiedLocals, // See WTHPFE.
      restackifiedLocals, // See WTHPFE.
      defaultRegion,
      currentHeight,
      pureHeight,
      additiveHeight)
  }

  def getClosuredDeclaredLocals(): Vector[IVariableT] = {
    parentEnv match {
      case n @ NodeEnvironmentT(_, _, _, _, _, _, _, _, _, _, _, _) => n.declaredLocals
      case f @ FunctionEnvironmentT(_, _, _, _, _, _, _, _, _, _) => f.getClosuredDeclaredLocals()
      case _ => Vector()
    }
  }

//  def getClosuredUnstackifiedLocals(): Vector[IVariableT] = {
//    parentEnv match {
//      case n @ NodeEnvironment(_, _, _, _, _, _, _) => n.unstackifiedLocals
//      case f @ FunctionEnvironment(_, _, _, _, _, _) => f.getClosuredDeclaredLocals()
//      case _ => Vector()
//    }
//  }

  // No particular reason we don't have an addFunction like PackageEnvironment does
}

case class FunctionEnvironmentBoxT(var functionEnvironment: FunctionEnvironmentT) extends IDenizenEnvironmentBoxT {
  override def currentHeight: Int = functionEnvironment.currentHeight
  override def pureHeight: Option[Int] = functionEnvironment.pureHeight
  override def additiveHeight: Option[Int] = functionEnvironment.additiveHeight

  override def equals(obj: Any): Boolean = vcurious(); override def hashCode(): Int = vfail() // Shouldnt hash, is mutable

  override def denizenTemplateId: IdT[ITemplateNameT] = functionEnvironment.denizenTemplateId
  override def denizenId: IdT[INameT] = functionEnvironment.denizenId

  override def snapshot: FunctionEnvironmentT = functionEnvironment
  def id: IdT[IFunctionNameT] = functionEnvironment.id
  def function: FunctionA = functionEnvironment.function
  def maybeReturnType: Option[CoordT] = functionEnvironment.maybeReturnType

//  override def defaultRegion: ITemplata[RegionTemplataType] = functionEnvironment.defaultRegion
  override def globalEnv: GlobalEnvironment = functionEnvironment.globalEnv
  override def templatas: TemplatasStore = functionEnvironment.templatas
  override def rootCompilingDenizenEnv: IInDenizenEnvironmentT = functionEnvironment.rootCompilingDenizenEnv

  def setReturnType(returnType: Option[CoordT]): Unit = {
    functionEnvironment = functionEnvironment.copy(maybeReturnType = returnType)
  }

  def addEntry(interner: Interner, name: INameT, entry: IEnvEntry): Unit = {
    functionEnvironment = functionEnvironment.addEntry(interner, name, entry)
  }
  def addEntries(interner: Interner, newEntries: Vector[(INameT, IEnvEntry)]): Unit= {
    functionEnvironment = functionEnvironment.addEntries(interner, newEntries)
  }

  override def lookupNearestWithImpreciseName(

    nameS: IImpreciseNameS,
    lookupFilter: Set[ILookupContext]):
  Option[ITemplataT[ITemplataType]] = {
    functionEnvironment.lookupNearestWithImpreciseName(nameS, lookupFilter)
  }

  override def lookupNearestWithName(

    nameS: INameT,
    lookupFilter: Set[ILookupContext]):
  Option[ITemplataT[ITemplataType]] = {
    functionEnvironment.lookupNearestWithName(nameS, lookupFilter)
  }

  override def lookupAllWithImpreciseName( nameS: IImpreciseNameS, lookupFilter: Set[ILookupContext]): Array[ITemplataT[ITemplataType]] = {
    functionEnvironment.lookupAllWithImpreciseName(nameS, lookupFilter)
  }

  override def lookupAllWithName( nameS: INameT, lookupFilter: Set[ILookupContext]): Iterable[ITemplataT[ITemplataType]] = {
    functionEnvironment.lookupAllWithName(nameS, lookupFilter)
  }

  override private[env] def lookupWithImpreciseNameInner( nameS: IImpreciseNameS, lookupFilter: Set[ILookupContext], getOnlyNearest: Boolean) = {
    functionEnvironment.lookupWithImpreciseNameInner(nameS, lookupFilter, getOnlyNearest)
  }

  override private[env] def lookupWithNameInner( nameS: INameT, lookupFilter: Set[ILookupContext], getOnlyNearest: Boolean): Array[ITemplataT[ITemplataType]] = {
    functionEnvironment.lookupWithNameInner(nameS, lookupFilter, getOnlyNearest)
  }

  def makeChildNodeEnvironment(node: IExpressionSE, life: LocationInFunctionEnvironmentT): NodeEnvironmentT = {
    functionEnvironment.makeChildNodeEnvironment(node, life)
  }

  // No particular reason we don't have an addFunction like PackageEnvironment does
}

sealed trait IVariableT  {
  def name: IVarNameT
  def variability: VariabilityT
  def coord: CoordT
}
sealed trait ILocalVariableT extends IVariableT {
  def name: IVarNameT
  def coord: CoordT
}
// Why the difference between reference and addressible:
// If we mutate/move a variable from inside a closure, we need to put
// the local's address into the struct. But, if the closures don't
// mutate/move, then we could just put a regular reference in the struct.
// Lucky for us, the parser figured out if any of our child closures did
// any mutates/moves/borrows.
case class AddressibleLocalVariableT(
  name: IVarNameT,
  variability: VariabilityT,
  coord: CoordT
) extends ILocalVariableT {
  val hash = runtime.ScalaRunTime._hashCode(this); override def hashCode(): Int = hash; override def equals(obj: Any): Boolean = vcurious();

}
case class ReferenceLocalVariableT(
  name: IVarNameT,
  variability: VariabilityT,
  coord: CoordT
) extends ILocalVariableT {
  val hash = runtime.ScalaRunTime._hashCode(this); override def hashCode(): Int = hash; override def equals(obj: Any): Boolean = vcurious();
  vpass()
}
case class AddressibleClosureVariableT(
  name: IVarNameT,
  closuredVarsStructType: StructTT,
  variability: VariabilityT,
  coord: CoordT
) extends IVariableT {
  vpass()
}
case class ReferenceClosureVariableT(
  name: IVarNameT,
  closuredVarsStructType: StructTT,
  variability: VariabilityT,
  coord: CoordT
) extends IVariableT {
  val hash = runtime.ScalaRunTime._hashCode(this); override def hashCode(): Int = hash; override def equals(obj: Any): Boolean = vcurious();

}

object EnvironmentHelper {
  def lookupWithNameInner(
    requestingEnv: IEnvironmentT,
    templatas: TemplatasStore,
    parent: IEnvironmentT,

    name: INameT,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    val result = templatas.lookupWithNameInner(requestingEnv, name, lookupFilter)
    if (result.nonEmpty && getOnlyNearest) {
      result.toArray
    } else {
      result.toArray ++ parent.lookupWithNameInner(name, lookupFilter, getOnlyNearest)
    }
  }

  def lookupWithImpreciseNameInner(
    requestingEnv: IEnvironmentT,
    templatas: TemplatasStore,
    parent: IEnvironmentT,

    name: IImpreciseNameS,
    lookupFilter: Set[ILookupContext],
    getOnlyNearest: Boolean):
  Array[ITemplataT[ITemplataType]] = {
    val result = templatas.lookupWithImpreciseNameInner(requestingEnv, name, lookupFilter)
    if (result.nonEmpty && getOnlyNearest) {
      result
    } else {
      result ++ parent.lookupWithImpreciseNameInner(name, lookupFilter, getOnlyNearest)
    }
  }
}