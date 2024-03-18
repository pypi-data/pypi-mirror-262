use std::sync::Arc;

use symbolica::{
    domains::{
        factorized_rational_polynomial::FactorizedRationalPolynomial, integer::IntegerRing,
        rational_polynomial::RationalPolynomial,
    },
    parser::Token,
    state::State,
};

fn univariate() {
    let var_names = vec!["x".into(), "y".into()];
    let var_map = Arc::new(
        var_names
            .iter()
            .map(|n| State::get_or_insert_var(n).into())
            .collect(),
    );

    let field = IntegerRing::new();

    let rat: RationalPolynomial<_, u8> = Token::parse("1/((x+1)*(x+2)(x^3+2x+1))")
        .unwrap()
        .to_rational_polynomial(&field, &field, &var_map, &var_names)
        .unwrap();

    println!("Partial fraction {}:", rat);
    for x in rat.apart(0) {
        println!("\t{}", x);
    }
}

fn multivariate() {
    let var_names = vec!["x".into(), "y".into()];
    let var_map = Arc::new(
        var_names
            .iter()
            .map(|n| State::get_or_insert_var(n).into())
            .collect(),
    );

    let field = IntegerRing::new();

    let rat: FactorizedRationalPolynomial<_, u8> = Token::parse("1/((x+y)*(x^2+x*y+1)(x+1))")
        .unwrap()
        .to_factorized_rational_polynomial(&field, &field, &var_map, &var_names)
        .unwrap();

    println!("Partial fraction {} in x:", rat);
    for x in rat.apart(0) {
        println!("\t{}", x);
    }
}

fn main() {
    univariate();
    multivariate();
}
