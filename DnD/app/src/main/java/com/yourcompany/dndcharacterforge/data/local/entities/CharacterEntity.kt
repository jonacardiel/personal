package com.yourcompany.dndcharacterforge.data.local.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "characters")
data class CharacterEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val name: String,
    val race: String,
    val classType: String,
    val level: Int
    // ... other character details ...
)
