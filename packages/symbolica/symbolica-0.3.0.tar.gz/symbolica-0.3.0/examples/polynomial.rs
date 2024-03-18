use symbolica::{
    domains::{
        finite_field::{FiniteField, FiniteFieldCore},
        rational::{Rational, RationalField},
    },
    poly::polynomial::MultivariatePolynomial,
};

fn main() {
    let field = RationalField::new();
    let mut a = MultivariatePolynomial::<RationalField, u8>::new(3, &field, Some(3), None);
    a.append_monomial(Rational::Natural(3, 4), &[1, 0, 0]);
    a.append_monomial(Rational::Natural(5, 1), &[1, 1, 0]);
    a.append_monomial(Rational::Natural(7, 3), &[1, 1, 2]);

    let mut b = MultivariatePolynomial::<RationalField, u8>::new(3, &field, Some(3), None);
    b.append_monomial(Rational::Natural(6, 7), &[0, 1, 0]);
    b.append_monomial(Rational::Natural(5, 1), &[1, 1, 0]);
    b.append_monomial(Rational::Natural(7, 3), &[1, 1, 2]);

    println!("> Polynomial multiplication: {} * {} =", a, b);
    println!("\t{}", a * &b);

    let finite_field = FiniteField::<u32>::new(17);
    let mut a =
        MultivariatePolynomial::<FiniteField<u32>, u8>::new(3, &finite_field, Some(3), None);
    a.append_monomial(finite_field.to_element(4), &[1, 0, 0]);
    a.append_monomial(finite_field.to_element(6), &[1, 1, 0]);
    a.append_monomial(finite_field.to_element(13), &[1, 1, 2]);

    let mut b =
        MultivariatePolynomial::<FiniteField<u32>, u8>::new(3, &finite_field, Some(3), None);
    b.append_monomial(finite_field.to_element(2), &[0, 1, 0]);
    b.append_monomial(finite_field.to_element(1), &[1, 1, 0]);
    b.append_monomial(finite_field.to_element(16), &[1, 1, 2]);

    println!("> Polynomial multiplication: {} * {} =", a, b);
    println!("\t{}", a * &b);
}
