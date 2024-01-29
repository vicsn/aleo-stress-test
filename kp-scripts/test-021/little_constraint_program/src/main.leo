// The 'little_constraint_program' program.
program little_constraint_program.aleo {
    transition main(input: field) -> field {
        let data: field = input * 1field;
        return data;
    }
}
