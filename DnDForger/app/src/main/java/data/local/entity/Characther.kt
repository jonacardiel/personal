package com.example.dndcharactermaker.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "characters")
data class Character(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    var name: String = "New Character",
    var playerName: String = "",
    var race: String = "",
    var subRace: String = "",
    var className: String = "", // For multiclassing, this will need a more complex structure
    var level: Int = 1,
    var background: String = "",
    var alignment: String = "",
    var experiencePoints: Int = 0,

    // Ability Scores
    var strength: Int = 10,
    var dexterity: Int = 10,
    var constitution: Int = 10,
    var intelligence: Int = 10,
    var wisdom: Int = 10,
    var charisma: Int = 10,

    // Combat
    var armorClass: Int = 10,
    var initiative: Int = 0,
    var speed: Int = 30,
    var maxHp: Int = 10,
    var currentHp: Int = 10,
    var tempHp: Int = 0,

    // Add fields for proficiencies, equipment, spells, etc. later
    // These are often best handled in separate related tables.
)