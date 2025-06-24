package com.dndforger.db

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.dndforger.model.Character
import com.dndforger.db.CharacterDao // Add this import

@Database(entities = [Character::class], version = 1)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun characterDao(): CharacterDao
}
