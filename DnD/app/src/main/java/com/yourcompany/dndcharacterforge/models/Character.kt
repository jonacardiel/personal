package com.yourcompany.dndcharacterforge.models

data class Character(
    val id: Int = 0,
    val name: String,
    val race: String,
    val classType: String,
    val level: Int
    // ... other character details ...
)
