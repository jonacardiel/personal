package com.dndforger.model

import java.io.Serializable

data class EquipmentItem(
    val name: String,
    val type: String,
    val quantity: Int,
    val weight: Double,
    val properties: String?,
    val notes: String?
) : Serializable
