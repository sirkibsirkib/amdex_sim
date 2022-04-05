#[derive(Debug, Eq, PartialEq, Ord, PartialOrd, Clone, Copy)]
struct Atom([u8; 16]);

#[derive(Debug, Eq, PartialEq, Ord, PartialOrd, Clone)]
struct Map(SortedVec<[Datum; 2]>);

impl Atom {
    fn incremented(mut self) -> Option<Self> {
        for byte in self.0.iter_mut() {
            *byte += 1;
            if *byte != 0 {
                // did not overflow
                return Some(self);
            }
        }
        None
    }
}
impl Map {
    fn key_fn(pair: &[Datum; 2]) -> &Datum {
        &pair[0]
    }
    fn last(&self) -> Option<&[Datum; 2]> {
        (self.0).0.last()
    }
    fn find(&self, key: &Datum) -> Result<usize, usize> {
        (self.0).0.binary_search_by(|key_in| key_in[0].cmp(key))
    }
    fn get(&self, key: &Datum) -> Option<&Datum> {
        self.find(key).ok().map(|i| &(self.0).0[i][1])
    }
    fn get_mut(&mut self, key: &Datum) -> Option<&mut Datum> {
        self.find(key).ok().map(|i| &mut (self.0).0[i][1])
    }
    fn first(&self) -> Option<&[Datum; 2]> {
        (self.0).0.first()
    }
    fn store(&mut self, value: Datum) -> Atom {
        for key_atom in AtomIter::default() {
            let key_datum = Datum::Atom(key_atom);
            if let Err(i) = self.find(&key_datum) {
                (self.0).0.insert(i, [key_datum, value]);
                return key_atom;
            }
        }
        unreachable!()
    }
}

struct AtomIter {
    next: Option<Atom>,
}
impl Default for AtomIter {
    fn default() -> Self {
        Self {
            next: Some(Atom([0; 16])),
        }
    }
}
impl Iterator for AtomIter {
    type Item = Atom;
    fn next(&mut self) -> Option<Atom> {
        let res = self.next?;
        self.next = res.incremented();
        Some(res)
    }
}

#[derive(Debug, Clone, Eq, PartialEq, Ord, PartialOrd)]
struct SortedVec<T: Ord>(Vec<T>);

#[derive(Debug, Eq, PartialEq, Ord, PartialOrd, Clone)]
enum Datum {
    Atom(Atom),
    Map(Map),
}

fn main() {
    println!("Hello, world!");
}
