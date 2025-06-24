package com.dndforger.model

import androidx.room.*
import java.io.Serializable

@Entity(tableName = "characters")
data class Character(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    var name: String,
    var race: String,
    var subrace: String?,
    var characterClass: String,
    var classLevels: Map<String, Int>, // For multiclassing: class name -> level
    var background: String,
    var alignment: String,
    var playerName: String,
    var experiencePoints: Int,
    @Embedded var abilityScores: AbilityScores,
    var skills: Map<String, Boolean>, // skill name -> proficiency
    var savingThrows: Map<String, Boolean>, // ability name -> proficiency
    var proficiencies: List<String>,
    var languages: List<String>,
    var equipment: List<EquipmentItem>,
    var spells: List<SpellSlot>,
    var features: List<String>,
    var feats: List<String>,
    var personalityTraits: String?,
    var ideals: String?,
    var bonds: String?,
    var flaws: String?,
    var backstory: String?,
    var allies: String?,
    var currency: Currency,
    var armorClass: Int,
    var initiative: Int,
    var speed: Int,
    var maxHp: Int,
    var currentHp: Int,
    var tempHp: Int,
    var hitDice: String,
    var deathSavesSuccess: Int,
    var deathSavesFailure: Int
) : Serializable
