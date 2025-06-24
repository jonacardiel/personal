package com.example.dndcharactermaker.ui.creation

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import com.example.dndcharactermaker.R
import com.example.dndcharactermaker.databinding.FragmentRaceSelectionBinding

class RaceSelectionFragment : Fragment() {

    private var _binding: FragmentRaceSelectionBinding? = null
    private val binding get() = _binding!!

    // Use activityViewModels to get the shared ViewModel
    private val creationViewModel: CharacterCreationViewModel by activityViewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentRaceSelectionBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Here you would populate a RecyclerView with races from your JSON data

        // Example with a simple button
        binding.buttonSelectDwarf.setOnClickListener {
            creationViewModel.selectRace("Dwarf", "Hill Dwarf")
        }

        binding.buttonNext.setOnClickListener {
            // Navigate to the next step in the creation flow
            findNavController().navigate(R.id.action_raceSelectionFragment_to_classSelectionFragment)
        }

        // Observe changes to the character to update the UI
        creationViewModel.characterInProgress.observe(viewLifecycleOwner) { character ->
            binding.textViewSelection.text = "Selected: ${character.race} (${character.subRace})"
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}