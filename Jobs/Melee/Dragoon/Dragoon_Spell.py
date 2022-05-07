from Jobs.Base_Spell import DOTSpell, empty
from Jobs.Melee.Dragoon.Dragoon_Player import Dragoon
from Jobs.Melee.Melee_Spell import DragoonSpell
import copy

#Requirement

def WheelingThrustRequirement(Player, Spell):
    return Player.WheelInMotion

def FangAndClawRequirement(Player, Spell):
    return Player.FangAndClaw

def LanceChargeRequirement(Player, Spell):
    return Player.LanceChargeCD <= 0

def BattleLitanyRequirement(Player, Spell):
    return Player.BattleLitanyCD <= 0

def DragonSightRequirement(Player, Spell):
    return Player.DragonSightCD <= 0

def GeirskogulRequirement(Player, Spell):
    return Player.GeirskogulCD <= 0

def NastrondRequirement(Player, Spell):
    return Player.LifeOfTheDragon and Player.NastrondCD <= 0

def HighJumpRequirement(Player, Spell):
    return Player.HighJumpCD <= 0

def MirageDiveRequirement(Player, Spell):
    return Player.DiveReady

def SpineshafterRequirement(Player, Spell):
    return Player.SpineshafterStack > 0

def LifeSurgeRequirement(Player, Spell):
    return Player.LifeSurgeStack > 0

#Apply

def ApplyTrueThrust(Player, Enemy):
    if not (TrueThrustCombo in Player.EffectList) : Player.EffectList.append(TrueThrustCombo)

def ApplyWheelingThrust(Player, Enemy):
    Player.WheelInMotion = False

def ApplyFangAndClaw(Player, Enemy):
    Player.FangAndClaw = False

def ApplyLanceCharge(Player, Enemy):
    Player.MultDPSBonus *= 1.1
    Player.LanceChargeCD = 60
    Player.LanceChargeTimer = 20
    Player.EffectCDList.append(LanceChargeCheck)

def ApplyBattleLitany(Player, Enemy):
    Player.BattleLitanyCD = 120
    Player.BattleLitanyTimer = 15

    #Will give each person in the fight the buff

    for player in Player.CurrentFight.PlayerList:  player.CritRateBonus += 0.1

    Player.EffectCDList.append(BattleLitanyCheck)

def ApplyGeirskogul(Player, Enemy):
    Player.GeirskogulCD = 30

    if Player.FullGaze : Player.LifeOfTheDragon = True

def ApplyHighJump(Player, Enemy):
    Player.HighJumpCD = 30
    Player.DiveReady = True

def ApplyMirageDive(Player, Enemy):
    Player.DiveReady = False
    Player.DragonGauge = min(2, Player.DragonGauge + 1)

def ApplySpineshafter(Player, Enemy):
    if Player.SpineshafterStack == 2:
        Player.EffectCDList.append(SpineshafterStackCheck)
        Player.SpineshafterCD = 60
    Player.SpineshafterStack -= 1

def ApplyLifeSurge(Player, Enemy):
    if Player.LifeSurgeStack == 2:
        Player.EffectCDList.append(LifeSurgeStackCheck)
        Player.LifeSurgeCD = 45
    Player.LifeSurgeStack -= 1

    Player.NextCrit = True

#Effect

def TrueThrustCombo(Player, Spell):
    if Spell.id == Disembowel.id:
        Spell.Potency += 110

        #Gain PowerSurge, 10% damage

        if Player.PowerSurgeTimer <= 0: #Not already applied
            Player.MultDPSBonus *= 1.10
            Player.EffectCDList.append(PowerSurgeCheck)
        Player.PowerSurgeTimer = 30

        Player.EffectList.append(DisembowelCombo)
        Player.EffectToRemove.append(TrueThrustCombo)

    elif Spell.id == VorpalThrust.id:
        Spell.Potency += 150
        Player.EffectList.append(VorpalThrustCombo)
        Player.EffectToRemove.append(TrueThrustCombo)

def VorpalThrustCombo(Player, Spell):
    if Spell.id == HeavenThrust.id:
        Spell.Potency += 380
        Player.FangAndClaw = True
        Player.EffectToRemove.append(VorpalThrustCombo)

def DisembowelCombo(Player, Spell):
    if Spell.id == ChaoticSpring.id:
        Spell.Potency +=160
        if Player.ChaoticSpringDOT == None:
            Player.ChaoticSpringDOT = copy.deepcopy(ChaoticSpringDOT)
            Player.DOTList.append(Player.ChaoticSpringDOT)
        Player.ChaoticSpringDOTTimer = 24

        Player.WheelInMotion = True 
        Player.EffectToRemove.append(DisembowelCombo)

def ApplyNastrond(Player, Spell):
    Player.NastrondCD = 10

#Check

def LifeSurgeStackCheck(Player, Enemy):
    if Player.LifeSurgeCD <= 0:
        if Player.LifeSurgeStack == 1:
            Player.EffectToRemove.append(LifeSurgeStackCheck)
        else:
            Player.LifeSurgeCD = 45
        Player.LifeSurgeStack += 1

def SpineshafterStackCheck(Player, Enemy):
    if Player.SpineshafterCD <= 0:
        if Player.SpineshafterStack == 1:
            Player.EffectToRemove.append(SpineshafterStackCheck)
        else:
            Player.SpineShifterCD = 60
        Player.SpineshafterStack += 1

def BattleLitanyCheck(Player, Enemy):
    if Player.BattleLitanyTimer <= 0:
        for player in Player.CurrentFight.PlayerList:  player.CritRateBonus -= 0.1 #Removing buff
        Player.EffectToRemove.append(BattleLitanyCheck)

def LanceChargeCheck(Player, Enemy):
    if Player.LanceChargeTimer <= 0:
        Player.MultDPSBonus /= 1.1
        Player.EffectToRemove.append(LanceChargeCheck)

def PowerSurgeCheck(Player, Enemy):
    if Player.PowerSurgeTimer <= 0:
        Player.EffectToRemove.append(PowerSurgeCheck)
        Player.MultDPSBonus /= 1.1

#GCD
#Combo Action
TrueThrust = DragoonSpell(1, True, 2.5, 230, ApplyTrueThrust, [], True)
Disembowel = DragoonSpell(2, True, 2.5, 140, empty, [], True)
VorpalThrust = DragoonSpell(3, True, 2.5, 130, empty, [], True)
ChaoticSpring = DragoonSpell(4, True, 2.5, 140, empty, [], True)
ChaoticSpringDOT = DOTSpell(-22, 45)
HeavenThrust = DragoonSpell(5, True, 2.5, 100, empty, [], True)

WheelingThrust = DragoonSpell(6, True, 2.5, 300, ApplyWheelingThrust, [WheelingThrustRequirement], True )
FangAndClaw = DragoonSpell(7, True, 2.5, 300, ApplyFangAndClaw, [FangAndClawRequirement], True)


#oGCD
LanceCharge = DragoonSpell(8, False, 0, 0, ApplyLanceCharge, [LanceChargeRequirement], False)
BattleLitany = DragoonSpell(9, False, 0, 0, ApplyBattleLitany, [BattleLitanyRequirement], False)
Geirskogul = DragoonSpell(11, False, 0, 260, ApplyGeirskogul, [GeirskogulRequirement], False)
Nastrond = DragoonSpell(12, False, 0, 300, ApplyNastrond, [NastrondRequirement], False)
HighJump = DragoonSpell(13, False, 0, 400, ApplyHighJump, [HighJumpRequirement], False)
MirageDive = DragoonSpell(14, False, 0, 200, ApplyMirageDive, [MirageDiveRequirement], False)
SpineshafterDive = DragoonSpell(15, False, 0, 250, ApplySpineshafter, [SpineshafterRequirement], False)
LifeSurge = DragoonSpell(16, False, 0, 0, ApplyLifeSurge, [LifeSurgeRequirement], False)

def DragonSight(Target):

    def DragonSightCheck(Player, Enemy):
        if Player.DragonSightTimer <= 0:
            Player.MultDPSBonus /= 1.1
            Target.MultDPSBonus /= 1.05
            Player.EffectToRemove.append(DragonSightCheck)

    def ApplyDragonSight(Player, Enemy):
        Player.DragonSightCD = 120
        Player.DragonSightTimer = 20

        Player.MultDPSBonus *= 1.1
        Target.MultDPSBonus *= 1.05
        Player.EffectCDList.append(DragonSightCheck)

    return DragoonSpell(10, False, 0, 0, ApplyDragonSight, [DragonSightRequirement], False)