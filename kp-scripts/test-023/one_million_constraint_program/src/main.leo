// The 'one_million_constraint_program' program.
program one_million_constraint_program.aleo {
    transition main(input: field) -> field {
        let data: field = input;
        for i:u8 in 0u8..6u8 {
            data = SHA3_256::hash_to_field(data);
        }
        for j:u8 in 0u8..90u8 {
            data = Poseidon8::hash_to_field(data);
        }
        return data;
    }
}
