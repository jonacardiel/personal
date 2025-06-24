package com.dndforger.model

import java.io.Serializable

data class SpellSlot(
    val level: Int,
    val knownSpells: List<String>,
    val preparedSpells: List<String>,
    val slotsTotal: Int,
    val slotsUsed: Int
) : Serializable
