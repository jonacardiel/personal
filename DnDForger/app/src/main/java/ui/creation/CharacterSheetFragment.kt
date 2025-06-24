class CharacterSheetFragment : Fragment() {
    // ... binding etc.
    private val args: CharacterSheetFragmentArgs by navArgs()
    private lateinit var sheetViewModel: CharacterSheetViewModel

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // You need a ViewModelFactory to pass the ID to the ViewModel
        // sheetViewModel = ViewModelProvider(this, factory).get(CharacterSheetViewModel::class.java)

        sheetViewModel.character.observe(viewLifecycleOwner) { character ->
            binding.characterName.text = character.name
            binding.characterRaceClass.text = "${character.race} ${character.className} ${character.level}"
            // ... update all other fields
        }

        sheetViewModel.strengthModifier.observe(viewLifecycleOwner) { modifier ->
            binding.strengthModifier.text = if (modifier >= 0) "+$modifier" else "$modifier"
        }
    }
}