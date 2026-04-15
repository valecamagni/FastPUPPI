import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, ExtVar
from L1Trigger.Phase2L1GMT.gmtTkMuons_cfi import gmtTkMuons

# --- LazyVar helper
def LazyVar(expr, valtype, doc=None, precision=-1):
    return Var(expr, valtype, doc, precision, lazyEval=True)

process = cms.Process("TEST")

# --- Input file
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/eos/cms/store/cmst3/group/l1tr/vcamagni/L1TauID/DATA/FPinputs/m20/4STEPS/142Xv0/inputs140X_7099344_3054.root'
    ),
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(200))

# --- L1 Tracker Muons GMT producer
process.l1tTkMuonsGmt = gmtTkMuons.clone(
    srcStubs  = cms.InputTag("l1tStubsGmt","tps"),
)

process.tkMuTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tTkMuonsGmt"),
    cut = cms.string(""),
    name = cms.string("TkMu"),
    doc = cms.string("TrackerMuons from GMT"),
    singleton = cms.bool(False),
    extension = cms.bool(False),
    variables = cms.PSet(
        pt        = LazyVar("phPt()",  float),
        eta       = LazyVar("phEta()", float),
        phi       = LazyVar("phPhi()", float),
        mass      = LazyVar("0.10566", float),
        z0        = LazyVar("phZ0()",  float, doc="Z coordinate of the reconstructed production vertex"),
        dxy       = LazyVar("phD0()",  float, doc="transverse impact parameter"),
        charge    = LazyVar("phCharge()", int, doc="charge"),
        quality   = LazyVar("hwQual()", int, doc="quality (TBD)"),
        hwPt      = LazyVar("hwPt()", int),
        hwEta     = LazyVar("hwEta()", int),
        hwPhi     = LazyVar("hwPhi()", int),
        hwZ0      = LazyVar("hwZ0()", int),
        hwD0      = LazyVar("hwD0()", int),
        hwCharge  = LazyVar("hwCharge()", int),
        hwIsoSum  = LazyVar("hwIsoSum()", int),
        hwIsoSumAp= LazyVar("hwIsoSumAp()", int)
    )
)

process.outnano = cms.OutputModule("NanoAODOutputModule",
    fileName = cms.untracked.string("tkmuons_nano.root"),
    outputCommands = cms.untracked.vstring(
        "drop *",                        # parte da vuoto
        "keep nanoaodFlatTable_*Table_*_*"  # prende tutte le SimpleCandidateFlatTable
    ),
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string("ZLIB")
)

# --- Path
process.p = cms.Path(process.l1tTkMuonsGmt + process.tkMuTable)
process.e = cms.EndPath(process.outnano)