#[cfg(feature = "test")]
#[macro_export]
macro_rules! day_input {
    ($day:literal) => {
        include_str!(concat!("../../../test-data/d", $day, ".txt"))
    };
}

#[cfg(not(feature = "test"))]
#[macro_export]
macro_rules! day_input {
    ($day:literal) => {
        include_str!(concat!("../../../data/d", $day, ".txt"))
    };
}
