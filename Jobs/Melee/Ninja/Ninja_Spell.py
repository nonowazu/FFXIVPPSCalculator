from Jobs.Base_Spell import buff, empty
from Jobs.Melee.Melee_Spell import NinjaSpell
from Jobs.Melee.Ninja.Ninja_Player import Ninja
Lock = 0.75


#Requirement

def PhantomKamaitachiRequirement(Player, Spell):
    return Player.PhantomKamaitachiReady, -1

def BunshinRequirement(Player, Spell):
    return Player.BunshinCD <=0 and Player.NinkiGauge >= 50, Player.BunshinCD

def TenRequirement(Player, Spell):
    if Player.Ten :
        Player.Ten = False
        return True, -1
    return False, -1

def ChiRequirement(Player, Spell):
    return Player.Chi, -1

def JinRequirement(Player, Spell):
    return Player.Jin, -1

def TenChiJinRequirement(Player, Spell):
    return Player.TenChiJinCD <= 0 and not Player.Kassatsu, Player.TenChiJinCD

def KassatsuOnRequirement(Player, Spell):
    return Player.Kassatsu, -1

def KassatsuRequirement(Player, Spell):
    return Player.KassatsuCD <= 0, Player.KassatsuCD

def NinjutsuRequirement(Player, Spell):
    return Player.NinjutsuStack > 0 or Player.Kassatsu, Player.NinjutsuCD

def FleetingRaijuRequirement(Player, Spell):
    return Player.RaijuStack > 0, -1

def MeisuiRequirement(Player, Spell):
    return Player.Suiton and Player.MeisuiCD <= 0, -1

def BhavacakraRequirement(Player, Spell):
    return Player.NinkiGauge >= 50, -1

def TrickAttackRequirement(Player, Spell):
    return Player.Suiton and Player.TrickAttackCD <= 0, -1

def MugRequirement(Player, Spell):
    return Player.MugCD <= 0, Player.MugCD

def DreamWithinADreamRequirement(Player, Spell):
    return Player.DreamWithinADreamCD <= 0, Player.DreamWithinADreamCD\

#Ninjutsu Requirement

#Ten 0
#Chi 1
#Jin 2

def FumaShurikenRequirement(Player, Spell):
    return Player.CurrentRitual == [0] or Player.CurrentRitual == [1] or Player.CurrentRitual == [2], -1

def RaitonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,1] or Player.CurrentRitual == [2,1], -1

def KatonRequirement(Player, Spell):
    return Player.CurrentRitual == [1,0] or Player.CurrentRitual == [2,0], -1

def HyotonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,2] or Player.CurrentRitual == [1,2], -1

def HutonRequirement(Player, Spell):
    return Player.CurrentRitual == [2,1,0] or Player.CurrentRitual == [1,2,0], -1

def DotonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,2,1] or Player.CurrentRitual == [2,0,1], -1

def SuitonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,1,2] or Player.CurrentRitual == [1,0,2], -1


#Apply

def ApplyTen(Player, Enemy):
    ApplyNinjutsu(Player, Enemy)
    Player.CurrentRitual.append(0) #0 is a Ten

def ApplyChi(Player, Enemy):
    ApplyNinjutsu(Player, Enemy)
    Player.CurrentRitual.append(1) #1 is a Chi

def ApplyJin(Player, Enemy):
    ApplyNinjutsu(Player, Enemy)
    Player.CurrentRitual.append(2) #2 is a Jin

def ApplyHide(Player, Enemy):
    Player.NinjutsuStack = 2

def ApplyPhantomKamaitachi(Player, Enemy):
    Player.PhantomKamaitachiReady = False
    Player.AddHuton(10)
    Player.AddNinki(10)

def ApplyBunshin(Player, Enemy):
    Player.AddNinki(-50)
    Player.BunshinCD = 90
    Player.BunshinStack = 5
    Player.EffectList.append(BunshinEffect)
    Player.PhantomKamaitachiReady = True
    Player.PhantomKamaitachiReadyTimer = 45
    Player.EffectCDList.append(PhantomKamaitachiCheck)

def ApplyTenChiJin(Player, Enemy):
    Player.TenChiJinCD = 120
    Player.TenChiJinTimer = 6
    Player.EffectCDList.append(TenChiJinCheck)
    Player.EffectList.append(TenChiJinEffect)

def ApplyKassatsu(Player, Enemy):
    Player.KassatsuTimer = 15
    Player.KassatsuCD = 60
    Player.Kassatsu = True
    Player.EffectList.append(KassatsuEffect)
    Player.EffectCDList.append(KassatsuCheck)

def ApplyHyoshoRanryu(Player, Enemy):
    Player.ResetRitual()

def ApplySuiton(Player, Enemy):
    Player.Suiton = True
    if not SuitonCheck in Player.EffectCDList : Player.EffectCDList.append(SuitonCheck)
    Player.SuitonTimer = 20
    Player.ResetRitual()

def ApplyHuton(Player, Enemy):
    Player.HutonTimer = 60
    if not (HutonEffect in Player.EffectList):
        Player.EffectList.append(HutonEffect)
    if not (HutonCheck in Player.EffectCDList):
        Player.EffectCDList.append(HutonCheck)
    Player.ResetRitual()

def ApplyRaiton(Player, Enemy):
    if Player.RaijuStack == 0: Player.EffectList.append(RaitonEffect) #will loose all if weaponskill is done
    Player.RaijuStack = min(3, Player.RaijuStack + 1)
    Player.ResetRitual()

def ApplyNinjutsu(Player, Enemy):
    if len(Player.CurrentRitual) == 0 or Player.Kassatsu: #If we are not already in a ritual
        if Player.NinjutsuStack == 2:
            Player.EffectCDList.append(NinjutsuStackCheck)
            Player.NinjutsuCD = 20
        Player.NinjutsuStack -= 1

def ApplyThrowingDagger(Player, Enemy):
    Player.AddNinki(5)

def ApplyFleetingRaiju(Player, Enemy):
    Player.RaijuReady = False
    Player.RaijuStack -= 1
    Player.AddNinki(5)
    

def ApplyMeisui(Player, Enemy):
    Player.Suiton = False
    Player.AddNinki(50)
    Player.MeisuiCD = 120
    Player.MeisuiTimer = 30
    Player.EffectList.append(MeisuiEffect)
    Player.EffectCDList.append(MeisuiCheck)

def ApplyBhavacakra(Player, Enemy):
    Player.AddNinki(-50)

def ApplyTrickAttack(Player, Enemy):
    Player.buffList.append(TrickAttackBuff)
    Player.TrickAttackCD = 60
    Player.TrickAttackTimer = 15
    Player.EffectCDList.append(TrickAttackCheck)

def ApplyMug(Player, Enemy):
    Enemy.buffList.append(MugBuff)
    Player.MugCD = 120
    Player.MugTimer = 20
    Player.AddNinki(40)
    Player.EffectCDList.append(MugCheck)

def ApplyHuraijin(Player, Enemy):
    Player.HutonTimer = 60

def ApplyDreamWithinADream(Player, Enemy):
    Player.DreamWithinADreamCD = 60

def ApplySpinningEdge(Player, Enemy):
    Player.AddNinki(5)
    
    if not (SpinningEdgeCombo in Player.EffectList): Player.EffectList.append(SpinningEdgeCombo)


#Effect

def TenChiJinEffect(Player, Spell):
    if Spell.id == Ten.id or Spell.id == Chi.id or Spell.id == Jin.id:
        if Spell.id == Ten.id:
            Player.CurrentRitual == 
    else:
        #Remove it
        Player.TenChiJinTimer = 0

def HutonEffect(Player, Spell):
    if isinstance(Spell, NinjaSpell) and Spell.Weaponskill : Spell.RecastTime *= 0.85

def BunshinEffect(Player, Spell):
    if isinstance(Spell, NinjaSpell) and Spell.Weaponskill:
        Spell.Potency += 160 #This is to make it simpler
        Player.BunshinStack -= 1
        Player.AddNinki(5)
        if Player.BunshinStack == 0:
            Player.EffectToRemove.append(BunshinEffect)

def KassatsuEffect(Player, Spell):
    if isinstance(Spell, NinjaSpell) and Spell.Ninjutsu:
        Spell.DPSBonus = 1.3
        Player.EffectCDList.remove(KassatsuCheck)
        Player.EffectToRemove.append(KassatsuEffect)
        Player.KassatsuTimer = 0

def RaitonEffect(Player, Spell):
    if (Spell.Weaponskill or Player.RaijuStack == 0) and Spell.id != FleetingRaiju.id:
        #input('removed')
        #print(Spell.id)
        Player.RaijuStack = 0
        Player.EffectToRemove.append(RaitonEffect)

def MeisuiEffect(Player, Spell):
    if Spell.id == Bhavacakra.id:
        Spell.Potency += 150

def SpinningEdgeCombo(Player, Spell):
    if Spell.id == GustSlash.id:
        Spell.Potency += 160
        Player.AddNinki(5)
        Player.EffectToRemove.append(SpinningEdgeCombo)
        if not (GustSlashCombo in Player.EffectList) : Player.EffectList.append(GustSlashCombo)

def GustSlashCombo(Player, Spell):
    if Spell.id == AeolianEdge.id:
        Spell.Potency += 240
        Player.AddNinki(15)
        Player.EffectToRemove.append(GustSlashCombo)
    elif Spell.id == ArmorCrush.id:
        Spell.Potency += 220
        Player.AddNinki(15)
        Player.AddHuton(30)
        Player.EffectToRemove.append(GustSlashCombo)


#Check

def HutonCheck(Player, Enemy):
    if Player.HutonTimer <= 0:
        Player.EffectList.remove(HutonEffect)
        Player.EffectToRemove.append(HutonCheck)

def PhantomKamaitachiCheck(Player, Enemy):
    if not Player.PhantomKamaitachiReady or Player.PhantomKamaitachiReadyTimer <= 0:
        Player.PhantomKamaitachiReady = False
        Player.PhantomKamaitachiReadyTimer = 0
        Player.EffectToRemove.append(PhantomKamaitachiCheck)

def SuitonCheck(Player, Enemy):
    if not Player.Suiton or Player.SuitonTimer <= 0:
        Player.EffectToRemove.append(SuitonCheck)
        Player.SuitonTimer = 0
        Player.Suiton = False

def KassatsuCheck(Player, Enemy):
    if Player.KassatsuTimer <= 0:
        #print("removed kassatsu")
        Player.EffectList.remove(KassatsuEffect)
        Player.EffectToRemove.append(KassatsuCheck)
        Player.Kassatsu = False

def NinjutsuStackCheck(Player, Enemy):
    if Player.NinjutsuCD <= 0:
        if Player.NinjutsuStack == 1:
            Player.EffectToRemove.append(NinjutsuStackCheck)
        else:
            Player.NinjutsuCD = 20
        Player.NinjutsuStack +=1

def MeisuiCheck(Player, Enemy):
    if Player.MeisuiTimer <= 0:
        Player.EffectList.remove(MeisuiEffect)
        Player.EffectToRemove.append(MeisuiCheck)

def TrickAttackCheck(Player, Enemy):
    if Player.TrickAttackTimer <= 0:
        Player.buffList.remove(TrickAttackBuff)
        Player.EffectToRemove.append(TrickAttackCheck)

def MugCheck(Player, Enemy):
    if Player.MugTimer <= 0:
        Enemy.buffList.remove(MugBuff)
        Player.EffectToRemove.append(MugCheck)



#GCD
SpinningEdge = NinjaSpell(1, True, Lock, 2.5, 220, ApplySpinningEdge, [], True, False)
GustSlash = NinjaSpell(2, True, Lock, 2.5, 160, empty, [], True, False)
AeolianEdge = NinjaSpell(3, True, Lock, 2.5, 200, empty, [], True, False)
ArmorCrush = NinjaSpell(4, True, Lock, 2.5, 200, empty, [], True, False)
Huraijin = NinjaSpell(6, True, Lock, 2.5, 200, ApplyHuraijin, [], True, False)
FleetingRaiju = NinjaSpell(11, True, Lock, 2.5, 560, ApplyFleetingRaiju, [FleetingRaijuRequirement], True, False)
ThrowingDagger = NinjaSpell(12, True, Lock, 2.5, 120, ApplyThrowingDagger, [], True, False)
PhantomKamaitachi = NinjaSpell(22, True, Lock, 2.5, 600, ApplyPhantomKamaitachi, [PhantomKamaitachiRequirement], True, False)

#Ninjutsu
FumaShuriken = NinjaSpell(13, True, Lock,1.5, 450, ApplyHyoshoRanryu, [FumaShurikenRequirement], False, True) #Same effect as HyoshoRanruy, since only reset Player.CurrentRitual list
Raiton = NinjaSpell(14, True, Lock,1.5, 650, ApplyRaiton, [RaitonRequirement], False, True )
Huton = NinjaSpell(15, True, Lock,1.5, 0, ApplyHuton, [HutonRequirement], False, True)
Suiton = NinjaSpell(16, True, Lock,1.5, 500, ApplySuiton, [SuitonRequirement], False, True)
HyoshoRanryu = NinjaSpell(17, True, Lock,1.5, 1300, ApplyHyoshoRanryu, [HyotonRequirement, KassatsuOnRequirement], False, True)

#Ritual
Ten = NinjaSpell(15, True, 1, 1, 0, ApplyTen, [NinjutsuRequirement], False, False)
Chi = NinjaSpell(15, True, 1, 1, 0, ApplyChi, [NinjutsuRequirement], False, False)
Jin = NinjaSpell(15, True, 1, 1, 0, ApplyJin, [NinjutsuRequirement], False, False)



#oGCD
TenChiJin = NinjaSpell(16, False, Lock, 0, 0, ApplyTenChiJin, [TenChiJinRequirement], False, False)
DreamWithinADream = NinjaSpell(5, False, Lock, 0, 3*150, ApplyDreamWithinADream, [DreamWithinADreamRequirement], False, False)
Mug = NinjaSpell(7, False, Lock, 0, 150, ApplyMug, [MugRequirement], False, False)
TrickAttack = NinjaSpell(8, False, Lock, 0, 400, ApplyTrickAttack, [TrickAttackRequirement], False, False)
Bhavacakra = NinjaSpell(9, False, Lock, 0, 350, ApplyBhavacakra, [BhavacakraRequirement], False, False)
Meisui = NinjaSpell(10, False, Lock, 0, 0, ApplyMeisui, [MeisuiRequirement], False, False)
Kassatsu = NinjaSpell(20, False, Lock, 0, 0, ApplyKassatsu,[KassatsuRequirement], False, False)
Bunshin = NinjaSpell(21, False, Lock, 0, 0, ApplyBunshin, [BunshinRequirement], False, False)
Hide = NinjaSpell(23, True, 0, 0, 0, ApplyHide, [], False, False)
#buff
MugBuff = buff(1.05)
TrickAttackBuff = buff(1.1)