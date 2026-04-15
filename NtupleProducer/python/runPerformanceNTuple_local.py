from FastPUPPI.NtupleProducer.runPerformanceNTuple import *
#process.Tracer = cms.Service("Tracer")
process.source = process.source.clone(
    fileNames = cms.untracked.vstring("root://eoscms.cern.ch//eos/cms/store/cmst3/group/l1tr/vcamagni/L1TauID/DATA/FPinputs/m20/4STEPS/142Xv0/inputs140X_7099344_3054.root")
    #fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/cmst3/group/l1tr/pviscone/SampleFactory/DoubleElectron_FlatPt_1To100__chain_Phase2Spring24GS-INFP_PU200/SampleFactory/250714_121635/inputs140X_103.root'),
    #fileNames = cms.untracked.vstring('file:inputs140X.root'),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200))

addTkEG()
addGenLep([11,13])
addGenVisTaus()
addGenVisTausConstituents(5)
addTkMu()
addNNPuppiTaus_v2()
addSeededConeJets()
addVertexes()
addJetConstituents(16)
saveCands()
