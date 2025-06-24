package com.yourcompany.dndcharacterforge.repository

import com.yourcompany.dndcharacterforge.data.local.dao.CharacterDao
import com.yourcompany.dndcharacterforge.data.local.entities.CharacterEntity
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

class CharacterRepository @Inject constructor(
    private val characterDao: CharacterDao
) {
    suspend fun insertCharacter(character: CharacterEntity) {
        characterDao.insertCharacter(character)
    }

    suspend fun updateCharacter(character: CharacterEntity) {
        characterDao.updateCharacter(character)
    }

    suspend fun deleteCharacter(character: CharacterEntity) {
        characterDao.deleteCharacter(character)
    }

    fun getAllCharacters(): Flow<List<CharacterEntity>> {
        return characterDao.getAllCharacters()
    }

    fun getCharacterById(id: Int): Flow<CharacterEntity?> {
        return characterDao.getCharacterById(id)
    }
}
