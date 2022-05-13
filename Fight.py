import math
from Enemy import Enemy
import matplotlib.pyplot as plt
import numpy as np


#Class
from Jobs.Caster.Caster_Player import Caster
from Jobs.Melee.Melee_Player import Melee
from Jobs.Ranged.Ranged_Player import Ranged
from Jobs.Tank.Tank_Player import Tank
from Jobs.Healer.Healer_Player import Healer

#Jobs
from Jobs.Caster.Blackmage.BlackMage_Player import BlackMage
from Jobs.Caster.Redmage.Redmage_Player import Redmage
from Jobs.Caster.Summoner.Summoner_Player import Summoner
from Jobs.Ranged.Bard.Bard_Player import Bard
from Jobs.Ranged.Dancer.Dancer_Player import Dancer

from Jobs.Tank.Paladin.Paladin_Player import Paladin
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import Gunbreaker
from Jobs.Tank.Warrior.Warrior_Player import Warrior
from Jobs.Tank.DarkKnight.DarkKnight_Player import Esteem, DarkKnight

from Jobs.Ranged.Machinist.Machinist_Player import Queen, Machinist

from Jobs.Melee.Samurai.Samurai_Player import Samurai
from Jobs.Melee.Ninja.Ninja_Player import Ninja
from Jobs.Melee.Dragoon.Dragoon_Player import Dragoon

from Jobs.Healer.Whitemage.Whitemage_Player import Whitemage
from Jobs.Healer.Scholar.Scholar_Player import Scholar
from Jobs.Healer.Astrologian.Astrologian_Player import Astrologian

class NoMoreAction(Exception):#Exception called if a spell fails to cast
    pass


#GCDReduction Effect

def GCDReductionEffect(Player, Spell):
    if Spell.GCD:
        Spell.CastTime *= Player.GCDReduction
        Spell.RecastTime *= Player.GCDReduction

class Fight:

    #This class will be the environment in which the fight happens. It will hold a list of players, an enemy, etc.
    # It will be called upon for when we want to start the simulation

    def __init__(self, PlayerList, Enemy):
        self.PlayerList = PlayerList
        self.Enemy = Enemy
        self.ShowGraph = True
        self.TimeStamp = 0
        self.TeamCompositionBonus = 1
    def PrintResult(self, time, TimeStamp):

        fig, axs = plt.subplots(1, 2, constrained_layout=True)
        axs[0].set_ylabel("DPS")
        axs[0].set_xlabel("Time (s)")
        axs[0].set_title("DPS over time")
        axs[0].spines["top"].set_alpha(0.0)
        axs[0].spines["right"].set_alpha(0.0)
        axs[0].set_facecolor("lightgrey")
        axs[1].set_ylabel("PPS")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_title("PPS over time")
        axs[1].spines["top"].set_alpha(0.0)
        axs[1].spines["right"].set_alpha(0.0)
        axs[1].set_facecolor("lightgrey")

        fig.suptitle("DPS and PPS values over time.")

        for player in self.PlayerList:
            print("The Total Potency done by player " + str(type(player)) + " was : " + str(player.TotalPotency))
            print("This same player had a Potency Per Second of: " + str(player.TotalPotency/time))
            print("This same Player had an average of " + str(player.TotalPotency/player.NextSpell) + " Potency/Spell")
            print("This same Player had an average of " + str(player.TotalPotency/(time/player.GCDTimer)) + " Potency/GCD")
            print("The DPS is : " + str(player.TotalDamage / time))
            print("=======================================================")

            #Plot part

            job = ""

            if isinstance(player, BlackMage) : job = "Blackmage"
            elif isinstance(player, Redmage) : job = "Redmage"
            elif isinstance(player, DarkKnight) : job = "DarkKnight"
            elif isinstance(player, Warrior) : job = "Warrior"
            elif isinstance(player, Paladin) : job = "Paladin"
            elif isinstance(player, Gunbreaker) : job = "Gunbreaker"
            elif isinstance(player, Machinist) : job = "Machinist"
            elif isinstance(player, Samurai) : job = "Samurai"
            elif isinstance(player, Ninja) : job = "Ninja"
            elif isinstance(player, Scholar) : job = "Scholar"
            elif isinstance(player, Whitemage) : job = "Whitemage"
            elif isinstance(player, Astrologian) : job = "Astrologian"
            elif isinstance(player, Summoner) : job = "Summoner"
            elif isinstance(player, Dragoon) : job = "Dragoon"
            elif isinstance(player, Bard) : 
                job = "Bard"
                print("==================")
                print("Expected Vs Used values for bard")
                print("Expected Refulgent Proc : " + str(player.ExpectedRefulgent) + " Used Refulgent Proc : " + str(player.UsedRefulgent))
                print("Expected Wanderer Repertoire Proc : " + str(player.ExpectedTotalWandererRepertoire) + " Used Repertoire Proc : " + str(player.UsedTotalWandererRepertoire))
                print("RepertoireAdd : " + str(player.UsedRepertoireAdd))
                print("Expected Soul Voice Gauge : " + str(player.ExpectedSoulVoiceGauge) + " Used SoulVoiceGauge : " + str(player.UsedSoulVoiceGauge))
                print("Expected BloodLetterReduction : " + str(player.ExpectedBloodLetterReduction) + " Used BloodLetterReduction : " + str(player.UsedBloodLetterReduction))
                print("==================")
            elif isinstance(player, Dancer):
                job = "Dancer"
                print("==================")
                print("Expected Vs Used Proc for Dancer")
                print("Expected SilkenSymettry : " + str(player.ExpectedSilkenSymettry) + " Used SilkenSymettry : " + str(player.UsedSilkenSymettry) )
                print("Expected SilkenFlow : " + str(player.ExpectedSilkenFlow) + " Used SilkenFlow : " + str(player.UsedSilkenFlow) )
                print("Expected FourfoldFeather : " + str(player.ExpectedFourfoldFeather) + " Used FourfoldFeather : " + str(player.UsedFourfoldFeather) )
                print("Expected ThreefoldFan : " + str(player.ExpectedThreefoldFan) + " Used ThreefoldFan : " + str(player.UsedThreefoldFan) )
                print("==================")
            axs[0].plot(TimeStamp,player.DPSGraph, label=job)
            axs[1].plot(TimeStamp,player.PotencyGraph, label=job)
        
        print("The Enemy has received a total potency of: " + str(self.Enemy.TotalPotency))
        print("The Potency Per Second on the Enemy is: " + str(self.Enemy.TotalPotency/time))
        print("The Enemy's total DPS is " + str(self.Enemy.TotalDamage / time))
        axs[0].xaxis.grid(True)
        axs[1].xaxis.grid(True)
        axs[0].xaxis.set_ticks(np.arange(2.5, max(TimeStamp)+1, 2.5))
        axs[1].xaxis.set_ticks(np.arange(2.5, max(TimeStamp)+1, 2.5))
        axs[0].legend()
        axs[1].legend()
        if self.ShowGraph: plt.show()



    def SimulateFight(self, TimeUnit, TimeLimit, FightCD):
            #This function will Simulate the fight given the enemy and player list of this Fight
            #It will increment in TimeUnit up to a maximum of TimeLimit (there can be other reasons the Fight ends)
            #It will check weither a player can cast its NextSpell, and if it can it will call the relevant functions
            #However, no direct computation is done in this function, it simply orchestrates the whole thing
            self.TimeStamp = 0   #Keep track of the time
            start = False

            timeValue = []  #Used for graph


            #The first thing we will do is compute the TEAM composition DPS bonus
            #each class will give 1%
            # Tank, Healer, Caster, Ranged, Melee
            hasMelee = False
            hasCaster = False
            hasRanged = False
            hasTank = False
            hasHealer = False
            for player in self.PlayerList:
                if isinstance(player, Melee) : hasMelee = True
                elif isinstance(player, Caster) : hasCaster = True
                elif isinstance(player, Ranged) : hasRanged = True
                elif isinstance(player, Tank) : hasTank = True
                elif isinstance(player, Healer) : hasHealer = True

            
            if hasMelee: self.TeamCompositionBonus += 0.01
            if hasCaster: self.TeamCompositionBonus += 0.01
            if hasRanged: self.TeamCompositionBonus += 0.01
            if hasTank: self.TeamCompositionBonus += 0.01
            if hasHealer: self.TeamCompositionBonus += 0.01

            #Will first compute each player's GCD reduction value based on their Spell Speed or Skill Speed Value

            for Player in self.PlayerList:
                Player.GCDReduction = (1000 - (130 * (Player.Stat["SS"]-400) / 1900))/1000
                Player.EffectList.append(GCDReductionEffect)

            while(self.TimeStamp <= TimeLimit):

                for player in self.PlayerList:
                    #print("MainStat : " + str(player.Stat["MainStat"]))
                    #Will first Check if the NextSpell is a GCD or not
                    if(not player.TrueLock and not Player.Casting):#If it is we do nothing
                        if(player.ActionSet[player.NextSpell].GCD):
                            print("Spell with id : " + str(player.ActionSet[player.NextSpell].id))
                            input("is being casted at : " + str(self.TimeStamp))
                            #Is a GCD

                            #Have to check if the player can cast the spell
                            #So check if Animation Lock, if Casting or if GCDLock
                            if(not (player.oGCDLock or player.GCDLock or player.Casting)):
                                #input("Current BUFF : "  + str(player.MultDPSBonus))
                                #If we in here, then we can cast the next spell
                                #print(player)
                                #input("is casting gcd at : " + str(self.TimeStamp))

                                player.CastingSpell = player.ActionSet[player.NextSpell].Cast(player, self.Enemy)#Cast the spell
                                #print("Spell with ID " + str(player.CastingSpell.id) + " has begun casting at " +  str(self.self.TimeStamp) )
                                #Locking the player

                                player.Casting = True
                                player.CastingLockTimer = player.CastingSpell.CastTime
                                player.GCDLock = True
                                player.GCDLockTimer = player.CastingSpell.RecastTime
                                player.CastingTarget = self.Enemy
                            #Else we do nothing since doing the nextspell is not currently possible


                        else:
                            #Is an oGCD
                            print("Spell with id : " + str(player.ActionSet[player.NextSpell].id))
                            input("is being casted at : " + str(self.TimeStamp))
                            
                            if(not (player.oGCDLock or player.Casting)):
                                #Then we can cast the oGCD
                                player.CastingSpell = player.ActionSet[player.NextSpell].Cast(player, self.Enemy)
                                player.CastingSpell.CastFinal(player, self.Enemy)
                                player.oGCDLock = True
                                player.oGCDLockTimer = player.CastingSpell.CastTime
                                #print("oGCD with ID " + str(player.CastingSpell.id) + " has begun casting at " +  str(self.TimeStamp) )


                    


                #Will then let the enemy add the Dots damage

                for player in self.PlayerList:
                    #print(player)
                    #print("============")
                    for DOT in player.DOTList:
                        DOT.CheckDOT(player,self.Enemy, TimeUnit)
                for player in self.PlayerList:
                    #print(player.EffectCDList)
                    for CDCheck in player.EffectCDList:
                        CDCheck(player, self.Enemy)
                    for remove in player.EffectToRemove:
                        player.EffectCDList.remove(remove) #Removing relevant spell

                    player.EffectToRemove = []
                


                #We will now update any timer each player and the enemy has

                for player in self.PlayerList:
                    player.updateTimer(TimeUnit)
                    player.updateCD(TimeUnit)
                    player.updateLock() #Update the lock on the player to see if it's state changes


                CheckFinalLock = True
                for player in self.PlayerList:
                    CheckFinalLock = player.TrueLock and CheckFinalLock #If all player's TrueLock is true, then CheckFinalLock will be True

                if CheckFinalLock: 
                    print("The Fight finishes at: " + str(self.TimeStamp))
                    break

                
                if start:
                    #If the fight has started, will sample DPS values at certain time
                    if (self.TimeStamp%1 == 0.3 or self.TimeStamp%1 == 0.0 or self.TimeStamp%1 == 0.6 or self.TimeStamp%1 == 0.9) and self.TimeStamp >= 3:#last thing is to ensure no division by zero and also to have no spike at the begining
                        #Only sample each 1/2 second
                        timeValue+= [self.TimeStamp]
                        for Player in self.PlayerList:
                            Player.DPSGraph += [round(Player.TotalDamage/self.TimeStamp, 2)] #Rounding the value to 2 digits
                            Player.PotencyGraph += [round(Player.TotalPotency/self.TimeStamp, 2)]

                #update self.TimeStamp
                self.TimeStamp += TimeUnit
                self.TimeStamp = round(self.TimeStamp, 2)

                FightCD -= TimeUnit
                if FightCD <= 0 and not start:
                    self.TimeStamp = 0
                    start = True
                    #print("==========================================================================================")
                    #print("FIGHT START")
                    #print("==========================================================================================")

            

            #Post fight computations

            #print("LIST========================================================")

            remove = []

            for i in range(len(self.PlayerList)):  
                player = self.PlayerList[i]
                if isinstance(player, DarkKnight):
                    player.TotalPotency += player.EsteemPointer.TotalPotency    #Adds every damage done by Esteem to the dark knight
                if isinstance(player, Queen):
                    remove += [i]
                if isinstance(player, Esteem):
                    remove += [i]

            k = 0
            for i in remove:
                self.PlayerList.pop(i-k)
                k+=1
                

            self.PrintResult(self.TimeStamp, timeValue)
            




def ComputeDamage(Player, Potency, Enemy, SpellBonus, type):

    #Still remains to change the f_MAIN_DAMAGE function for pets

    #The type input signifies what type of damage we are dealing with, since the computation will chance according to what
    #type of damage it is

    #type = 0 (Direct Damage), type = 1 (magical DOT), type = 2(physical DOT), type = 3 (Auto-attacks)

    #All relevant formulas were taken from https://finalfantasy.fandom.com/wiki/Final_Fantasy_XIV_attributes#Damage_and_healing_formulae
    #The formulas on the website assume a random function that will randomise the ouput. We instead compute the expected outcome.
    #Also thanks to whoever did the DPS computation code on the black mage gear comparison sheet : https://docs.google.com/spreadsheets/d/1t3EYSOPuMceqCFrU4WAbzSd4gbYi-J7YeMB36dNmaWM/edit#gid=654212594
    #It helped me a lot to understand better the DPS computation of this game
    #Also, note that this function is still in development, and so some of these formulas might be a bit off. Use at your own risk.
    #This function will compute the DPS given the stats of a player

    levelMod = 1900
    baseMain = 390  
    baseSub = 400#Level 90 LevelMod values

    JobMod = Player.JobMod #Level 90 jobmod value, specific to each job

    Enemy = Player.CurrentFight.Enemy #Enemy targetted

    MainStat = Player.Stat["MainStat"] * Player.CurrentFight.TeamCompositionBonus #Scaling %bonus on mainstat

    #Computing values used throughout all computations
    
    f_WD = (Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))/100
    if isinstance(Player, Tank) : f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*145/baseMain))/100 #This is experimental, and I do not have any actual proof to back up, but tanks do have a different f_MAIN_DMG formula
    else: f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*195/baseMain))/100

    f_DET = math.floor(1000+math.floor(130*(Player.Stat["Det"]-baseMain)/levelMod))/1000#Determination damage

    if isinstance(Player, Tank) : f_TEN = (1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000 #Tenacity damage, 1 for non-tank player
    else : f_TEN = 1 #if non-tank
    f_SPD = (1000+math.floor(130*(Player.Stat["SS"]-baseSub)/levelMod))/1000 #Used only for dots

    CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000 #Crit rate in decimal

    CritDamage = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000 #Crit Damage multiplier

    DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000 #DH rate in decimal

    if Enemy.ChainStratagem: CritRate += 0.1    #If ChainStratagem is active, increase crit rate

    if Enemy.WanderingMinuet: CritRate += 0.02 #If WanderingMinuet is active, increase crit rate

    if Enemy.BattleVoice: DHRate += 0.2 #If WanderingMinuet is active, increase DHRate


    DHRate += Player.DHRateBonus #Adding Bonus
    CritRate += Player.CritRateBonus #Adding bonus

    if isinstance(Player, Machinist): 
        #print(Player.ActionSet[Player.NextSpell])  #Then if machinist, has to check if direct crit guarantee
        if Player.ActionSet[Player.NextSpell].id != -1 and Player.ActionSet[Player.NextSpell].id != -2 and Player.Reassemble and Player.ActionSet[Player.NextSpell].WeaponSkill:    #Checks if reassemble is on and if its a weapon skill
            CritRate = 1
            DHRate = 1
            Player.Reassemble = False #Uses Reassemble       
    elif isinstance(Player, Warrior):
        if Player.InnerReleaseStack >= 1 and (Player.NextSpell < len(Player.ActionSet)) and (Player.ActionSet[Player.NextSpell].id == 9 or Player.ActionSet[Player.NextSpell].id == 8):
            CritRate = 1#If inner release weaponskill
            DHRate = 1
            Player.InnerReleaseStack -= 1
    elif isinstance(Player, Samurai):
        if Player.DirectCrit:
            CritRate = 1
            DHRate = 1
            Player.DirectCrit = False
    elif isinstance(Player, Dancer):
        if Player.NextDirectCrit:
            CritRate = 1
            DHRate = 1
            Player.NextDirectCrit = False
    elif isinstance(Player, Dragoon):
        if Player.NextCrit and Player.ActionSet[Player.NextSpell].Weaponskill: #If next crit and weaponskill
            CritRate = 1
            Player.NextCrit = False

    if type == 0: #Type 0 is direct damage
        Damage = math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN ) *f_WD) * Player.Trait) #Player.Trait is trait DPS bonus
        #We will average the DPS by using DHRate, CritRate and CritDamage multiplier
        Damage = math.floor(math.floor(Damage * (1 + (CritRate * CritDamage)) ) * (1 + (DHRate * 0.25))) #Average DHRate and Crit contribution
        Damage = math.floor(Damage * SpellBonus)

    elif type == 1 : #Type 1 is magical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_WD) * f_MAIN_DMG) * f_SPD) * f_DET) * f_TEN) * Player.Trait) + 1
        Damage = math.floor(math.floor(Damage * (1 + (CritRate * CritDamage)) ) * (1 + (DHRate * 0.25))) #Average DHRate and Crit contribution

    elif type == 2: #Physical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN) * f_SPD) * f_WD) * Player.Trait) +1
        Damage = math.floor(math.floor(Damage * (1 + (CritRate * CritDamage)) ) * (1 + (DHRate * 0.25))) #Average DHRate and Crit contribution
    elif type == 3: #Auto-attacks
        Damage = math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN) * f_SPD)
        Damage = math.floor(math.floor(Damage * math.floor(f_WD * (Player.Delay/3) *100 )/100) * Player.Trait)
        Damage = math.floor(math.floor(Damage * (1 + (CritRate * CritDamage)) ) * (1 + (DHRate * 0.25))) #Average DHRate and Crit contribution

    #Now applying buffs

    for buffs in Player.buffList: 
        Damage = math.floor(Damage * buffs.MultDPS) #Multiplying all buffs
        
    for buffs in Enemy.buffList:
        Damage = math.floor(Damage * buffs.MultDPS) #Multiplying all buffs

    return Damage

"""
#Original ComputeDamage function

def ComputeDamageV2(Player, DPS, EnemyBonus, SpellBonus):
    #This function will compute the DPS given the stats of a player

    levelMod = 1900
    baseMain = 390  
    baseSub = 400
    JobMod = Player.JobMod

    MainStat = Player.Stat["MainStat"] * Player.CurrentFight.TeamCompositionBonus #Scaling %bonus

    Damage=math.floor(DPS*(Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))*(100+math.floor((MainStat-baseMain)*195/baseMain))/100)

    Damage=math.floor(Damage*(1000+math.floor(140*(Player.Stat["Det"]-baseMain)/levelMod))/1000)#Determination damage

    Damage=math.floor(Damage*(1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000)#Tenacity damage

    Damage=math.floor(Damage*(1000+math.floor(130*(Player.Stat["SS"]-baseSub)/levelMod))/1000)#Spell/Skill speed damage bonus, only on DOT

    Damage = math.floor(Damage * EnemyBonus * SpellBonus)
    #input("Damage inside v1.0 : " + str(Damage))

    CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000

    CritDamage = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000

    DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000

    if Player.CurrentFight.Enemy.ChainStratagem: CritRate += 0.1    #If ChainStratagem is active, increase crit

    if Player.CurrentFight.Enemy.WanderingMinuet: CritRate += 0.02 #If WanderingMinuet is active, increase crit

    if Player.CurrentFight.Enemy.BattleVoice: DHRate += 0.2 #If WanderingMinuet is active, increase crit


    

    DHRate += Player.DHRateBonus #Adding Bonus
    CritRate += Player.CritRateBonus #Adding bonus

    if isinstance(Player, Machinist): 
        #print(Player.ActionSet[Player.NextSpell])  #Then if machinist, has to check if direct crit guarantee
        if Player.ActionSet[Player.NextSpell].id != -1 and Player.ActionSet[Player.NextSpell].id != -2 and Player.Reassemble and Player.ActionSet[Player.NextSpell].WeaponSkill:    #Checks if reassemble is on and if its a weapon skill
            CritRate = 1
            DHRate = 1
            Player.Reassemble = False #Uses Reassemble       
    elif isinstance(Player, Warrior):
        if Player.InnerReleaseStack >= 1 and (Player.ActionSet[Player.NextSpell].id == 9 or Player.ActionSet[Player.NextSpell].id == 8):
            CritRate = 1#If inner release weaponskill
            DHRate = 1
            Player.InnerReleaseStack -= 1
    elif isinstance(Player, Samurai):
        if Player.DirectCrit:
            CritRate = 1
            DHRate = 1
            Player.DirectCrit = False
    elif isinstance(Player, Dancer):
        if Player.NextDirectCrit:
            CritRate = 1
            DHRate = 1
            Player.NextDirectCrit = False
    elif isinstance(Player, Dragoon):
        if Player.NextCrit and Player.ActionSet[Player.NextSpell].Weaponskill: #If next crit and weaponskill
            CritRate = 1
            Player.NextCrit = False

    return round(Damage * ((1+(DHRate/4))*(1+(CritRate*CritDamage)))/100, 2)

    // Pulled from Orinx's Gear Comparison Sheet with slight modifications
function Damage(Potency, WD, JobMod, MainStat,Det, Crit, DH,SS,TEN, hasBrd, hasDrg, hasSch, hasDnc, classNum) {
  
  MainStat=Math.floor(MainStat*(1+0.01*classNum));
  var Damage=Math.floor(Potency*(WD+Math.floor(baseMain*JobMod/1000))*(100+Math.floor((MainStat-baseMain)*195/baseMain))/100);
  Damage=Math.floor(Damage*(1000+Math.floor(140*(Det-baseMain)/levelMod))/1000);
  Damage=Math.floor(Damage*(1000+Math.floor(100*(TEN-baseSub)/levelMod))/1000);
  Damage=Math.floor(Damage*(1000+Math.floor(130*(SS-baseSub)/levelMod))/1000/100);
  Damage=Math.floor(Damage*magicAndMend)
  Damage=Math.floor(Damage*enochian)
  var CritDamage=CalcCritDamage(Crit)
  var CritRate=CalcCritRate(Crit) + (hasDrg ? battleLitanyAvg : 0) + (hasSch ? chainStratAvg : 0) + (hasDnc ? devilmentAvg : 0) + (hasBrd ? brdCritAvg : 0);
  var DHRate=CalcDHRate(DH) + (hasBrd ? battleVoiceAvg + brdDhAvg : 0) + (hasDnc ? devilmentAvg : 0);
  return Damage * ((1+(DHRate/4))*(1+(CritRate*CritDamage)))                                                                                                                               
}

"""