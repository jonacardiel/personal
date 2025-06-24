package com.yourcompany.dndcharacterforge.di

import com.yourcompany.dndcharacterforge.data.local.dao.CharacterDao
import com.yourcompany.dndcharacterforge.repository.CharacterRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {

    @Provides
    @Singleton
    fun provideCharacterRepository(characterDao: CharacterDao): CharacterRepository {
        return CharacterRepository(characterDao)
    }
}
