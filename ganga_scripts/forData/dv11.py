from os import environ
from GaudiKernel.SystemOfUnits import *
from Gaudi.Configuration import *
from Configurables import GaudiSequencer, CombineParticles 
from PhysConf.Selections import AutomaticData, MomentumScaling, TupleSelection
from Configurables import DecayTreeTuple, EventTuple, TupleToolTrigger, TupleToolTISTOS,FilterDesktop
from Configurables import BackgroundCategory, TupleToolDecay, TupleToolVtxIsoln,TupleToolPid,EventCountHisto,TupleToolRecoStats,TupleToolDecayTreeFitter,SubstitutePID
from Configurables import LoKi__Hybrid__TupleTool, TupleToolVeto,TriggerTisTos
from DecayTreeTuple.Configuration import *
# Unit
mtl= [
        "L0HadronDecision",
        "Hlt1TrackAllL0Decision",
        "Hlt1TrackMVADecision",
        "Hlt1TwoTrackMVADecision",

        "Hlt2Topo2BodyDecision",
        "Hlt2Topo3BodyDecision",
        "Hlt2Topo4BodyDecision",
        "Hlt2Topo2BodyBBDTDecision",
        "Hlt2Topo3BodyBBDTDecision",
        "Hlt2Topo4BodyBBDTDecision",
]
importOptions("$STDOPTS/PreloadUnits.opts")
def fillDecayTreeFitter(dtt,constr):
    i=dtt

    i.addTool(TupleToolDecay, name = 'B')
    i.ToolList += [ "TupleToolKinematic" ,"TupleToolRecoStats","TupleToolGeometry" ,"TupleToolDira" ,"TupleToolPid" ,"TupleToolPropertime" ,"TupleToolEventInfo" ,"TupleToolTrackInfo" ]

    i.ToolList+=[ "TupleToolTISTOS" ]
    i.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    i.TupleToolTISTOS.Verbose=True
    i.TupleToolTISTOS.VerboseHlt1=True
    i.TupleToolTISTOS.VerboseHlt2=True
    i.TupleToolTISTOS.TriggerList = mtl

    i.B.ToolList +=  [ "TupleToolDecayTreeFitter/PVFit"]       
    i.B.addTool(TupleToolDecayTreeFitter("PVFit"))
    i.B.PVFit.Verbose = True
    i.B.PVFit.UpdateDaughters= True
    i.B.PVFit.constrainToOriginVertex = True
    i.B.PVFit.daughtersToConstrain = constr[:-1]

    i.B.ToolList +=  [ "TupleToolDecayTreeFitter/PVFitB"]       
    i.B.addTool(TupleToolDecayTreeFitter("PVFitB"))
    i.B.PVFitB.Verbose = True
    i.B.PVFitB.UpdateDaughters= True
    i.B.PVFitB.constrainToOriginVertex = True
    i.B.PVFitB.daughtersToConstrain = [constr[-1]]

    i.B.ToolList +=  [ "TupleToolDecayTreeFitter/PVFitA"]        ###all
    i.B.addTool(TupleToolDecayTreeFitter("PVFitA"))
    i.B.PVFitA.Verbose = True
    i.B.PVFitA.UpdateDaughters= True
    i.B.PVFitA.constrainToOriginVertex = True
    i.B.PVFitA.daughtersToConstrain = constr

#
flts=[]
dtts=[]
###########

###########
loc2DD="Phys/B2D0DKSDDBeauty2CharmLine/Particles"
loc2LL="Phys/B2D0DKSLLBeauty2CharmLine/Particles"
FltB2DD0K02h= FilterDesktop("FltB2DD0K02h")
FltB2DD0K02h.Code = " (1==NINTREE((ID=='K+')&(PROBNNk>0.2)&(MIPCHI2DV(PRIMARY)>6.0)&(PT>300.*MeV))) &(1==NINTREE((ID=='K-')&(PROBNNk>0.2)&(MIPCHI2DV(PRIMARY)>6.0)&(PT>300.*MeV))) &(1==NINTREE((ABSID=='D0')&(M>1815.*MeV)&(M<1925.*MeV))) &(1==NINTREE((ABSID=='D+')&(M>1815.*MeV)&(M<1925.*MeV))) &(M>5000.*MeV)&(M<6000.*MeV)"
FltB2DD0K02h.Inputs = [loc2LL,loc2DD]
FltB2DD0K02h.Output= "Phys/FltB2DD0K02h/Particles" 
FltB2DD0K02h.RootInTES = "/Event/Bhadron" 
flts.append(FltB2DD0K02h)


FltB2DD0K02h_data = AutomaticData("Phys/FltB2DD0K02h/Particles")
FltB2DD0K02h_data = MomentumScaling( FltB2DD0K02h_data)

FltB2DD0K02h_tuple = TupleSelection("B2DD0K02h",
        [FltB2DD0K02h_data],
        Decay = "[Beauty -> ^(D+  -> ^K- ^pi+ ^pi+) ^(Charm -> ^K+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC" ,
        Branches = {
        "B"          :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D1"          :"[Beauty -> ^(D+  -> K- pi+ pi+) (Charm -> K+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D1K"         :"[Beauty -> (D+  -> ^K- pi+ pi+) (Charm -> K+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D1H1"       :"[Beauty -> (D+  -> K- pi+ ^pi+) (Charm -> K+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D1H2"       :"[Beauty -> (D+  -> K- ^pi+ pi+) (Charm -> K+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D2"         :"[Beauty -> (D+  -> K- pi+ pi+) ^(Charm -> K+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D2H"       :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ ^pi-) (KS0 -> pi+ pi-)]CC", 
        "D2K"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> ^K+ pi-) (KS0 -> pi+ pi-)]CC", 
        "KS0"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi-) ^(KS0 -> pi+ pi-)]CC", 
        "Pip"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi-) (KS0 -> ^pi+ pi-)]CC", 
        "Pim"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi-) (KS0 -> pi+ ^pi-)]CC", 
    }
        )
tFltB2DD0K02h = FltB2DD0K02h_tuple.algorithm()
fillDecayTreeFitter(tFltB2DD0K02h,["KS0","D+","D0","B+"])
from PhysConf.Selections import SelectionSequence
seqFltB2DD0K02h_data = SelectionSequence('SEQ1', FltB2DD0K02h_tuple)
###########
loc2DD="Phys/B2D0DKSDDD02K3PiBeauty2CharmLine/Particles"
loc2LL="Phys/B2D0DKSLLD02K3PiBeauty2CharmLine/Particles"
FltB2DD0K04h= FilterDesktop("FltB2DD0K04h")
FltB2DD0K04h.Code = " (1==NINTREE((ID=='K+')&(PROBNNk>0.2)&(MIPCHI2DV(PRIMARY)>6.0)&(PT>300.*MeV))) &(1==NINTREE((ID=='K-')&(PROBNNk>0.2)&(MIPCHI2DV(PRIMARY)>6.0)&(PT>300.*MeV))) &(1==NINTREE((ABSID=='D0')&(M>1815.*MeV)&(M<1925.*MeV))) &(1==NINTREE((ABSID=='D+')&(M>1815.*MeV)&(M<1925.*MeV))) &(M>5000.*MeV)&(M<6000.*MeV)"
FltB2DD0K04h.Inputs = [loc2LL,loc2DD]
FltB2DD0K04h.Output= "Phys/FltB2DD0K04h/Particles" 
FltB2DD0K04h.RootInTES = "/Event/Bhadron" 
flts.append(FltB2DD0K04h)


FltB2DD0K04h_data = AutomaticData("Phys/FltB2DD0K04h/Particles")
FltB2DD0K04h_data = MomentumScaling( FltB2DD0K04h_data)

FltB2DD0K04h_tuple = TupleSelection("B2DD0K04h",
        [FltB2DD0K04h_data],
        Decay = "[Beauty -> ^(D+  -> ^K- ^pi+ ^pi+) ^(Charm -> ^K+ ^pi- ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC", 
         Branches = {
        "D1"          :"[Beauty -> ^(D+  -> K- pi+ pi+) (Charm -> K+ pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D1K"         :"[Beauty -> (D+  -> ^K- pi+ pi+) (Charm -> K+ pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D1H1"       :"[Beauty -> (D+  -> K- pi+ ^pi+) (Charm -> K+ pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D1H2"       :"[Beauty -> (D+  -> K- ^pi+ pi+) (Charm -> K+ pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D2"         :"[Beauty -> (D+  -> K- pi+ pi+) ^(Charm -> K+ pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D2H"       :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ ^pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D2K"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> ^K+ pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D2Hp"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi- ^pi+ pi-) (KS0 -> pi+ pi-)]CC", 
        "D2Hm"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi- pi+ ^pi-) (KS0 -> pi+ pi-)]CC", 
        "KS0"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi- pi+ pi-) ^(KS0 -> pi+ pi-)]CC", 
        "Pip"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi- pi+ pi-) (KS0 -> ^pi+ pi-)]CC", 
        "Pim"        :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi- pi+ pi-) (KS0 -> pi+ ^pi-)]CC", 
        "B"          :"[Beauty -> (D+  -> K- pi+ pi+) (Charm -> K+ pi- pi+ pi-) (KS0 -> pi+ pi-)]CC", 
    }
         )

tFltB2DD0K04h = FltB2DD0K04h_tuple.algorithm()
fillDecayTreeFitter(tFltB2DD0K04h,["KS0","D+","D0","B+"])
from PhysConf.Selections import SelectionSequence
seqFltB2DD0K04h_data = SelectionSequence('SEQ2', FltB2DD0K04h_tuple)

###################





from PhysConf.Filters import LoKi_Filters
code=("|".join(["HLT_PASS('Stripping%sBeauty2CharmLineDecision')"]*10))%("B02D0D0KSD02HHD02HHLL","B02D0D0KSD02HHD02HHDD","B02D0D0KSD02HHD02K3PiLL","B02D0D0KSD02HHD02K3PiDD","B02D0D0KSD02K3PiD02K3PiLL","B02D0D0KSD02K3PiD02K3PiDD","B2D0DKSDD","B2D0DKSLL","B2D0DKSDDD02K3Pi","B2D0DKSLLD02K3Pi")

evtFilters = LoKi_Filters( STRIP_Code = code)

#SeqPhys.Members  += [Filter1]
#SeqPhys.Members += [MakeLb2LcH]

########################################################################
from Configurables import DaVinci
DaVinci().EventPreFilters = evtFilters.filters ('Filters')
DaVinci().EvtMax = -1
DaVinci().PrintFreq = 1000
DaVinci().SkipEvents = 0                       # Events to skip
DaVinci().DataType = "2011"
DaVinci().Simulation   = False 
DaVinci().Lumi =True 
DaVinci().HistogramFile = "DVHistos.root"      # Histogram file
DaVinci().TupleFile = "Tuple.root"             # Ntuple#
DaVinci().InputType = "MDST"
DaVinci().RootInTES = "/Event/Bhadron"
DaVinci().UserAlgorithms = flts+[seqFltB2DD0K02h_data,seqFltB2DD0K04h_data]
#DaVinci().Input=["/eos/lhcb/grid/prod/lhcb/LHCb/Collision18/BHADRON.MDST/00077054/0000/00077054_00009881_1.bhadron.mdst"]
