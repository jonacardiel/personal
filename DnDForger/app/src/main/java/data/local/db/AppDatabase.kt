package com.example.dndcharactermaker.data.local.db

import androidx.room.Database
import androidx.room.RoomDatabase
import com.example.dndcharactermaker.data.local.dao.CharacterDao
import com.example.dndcharactermaker.data.local.entity.Character

@Database(entities = [Character::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun characterDao(): CharacterDao
}