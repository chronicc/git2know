use std::env;
use std::io;
use std::fs::{self, DirEntry};
use std::path::{Path, PathBuf};

fn exec_on_dir_tree(path: &Path) -> io::Result<Vec<PathBuf>> {
    let mut dirs: Vec<PathBuf> = Vec::<PathBuf>::new();
    if path.is_dir() {
        for entry in fs::read_dir(path)? {
            let entry: DirEntry = entry?;
            let path: PathBuf = entry.path();
            if path.is_dir() {
                dirs.push(path);
                dirs.extend(exec_on_dir_tree(&path)?);
            }
        }
        return Ok(dirs);
    }
    Ok(dirs)
}

fn main() -> io::Result<()> {
    // let mut env_home_value: String = String::new();
    // match env::var("HOME") {
    //     Ok(val) => env_home_value = val,
    //     Err(env::VarError::NotPresent) => {
    //         eprintln!("HOME not set");
    //     },
    //     Err(env::VarError::NotUnicode(raw)) => {
    //         eprintln!("HOME not valid unicode: {:?}", raw);
    //     },
    // };
    // let path: &Path = Path::new(&env_home_value);
    let path: &Path = Path::new("/home/chronicc/git/chronicc/git2know");
    let files = match exec_on_dir_tree(path) {
        Ok(val) => val,
        Err(e) => {
            eprintln!("Error: {}", e);
            Vec::<PathBuf>::new()
        },
    };
    println!("Amount of found files: {}", files.len());
    Ok(())
}
