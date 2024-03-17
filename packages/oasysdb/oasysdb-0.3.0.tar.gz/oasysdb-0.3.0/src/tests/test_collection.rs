use super::*;

#[test]
fn build_large() {
    let len = 10000;
    let records = Record::many_random(DIMENSION, len);
    let config = Config::default();
    let collection = Collection::build(&config, &records).unwrap();
    assert_eq!(collection.len(), len);
}

#[test]
fn insert() {
    let mut collection = create_collection();

    // Create a new record to insert.
    let new_record = Record::random(DIMENSION);
    collection.insert(&new_record).unwrap();

    // Assert the new record is in the collection.
    let id = VectorID::from(LEN);
    assert_eq!(collection.len(), LEN + 1);
    assert_eq!(collection.get(&id).unwrap().data, new_record.data);
}

#[test]
fn insert_invalid_dimension() {
    let mut collection = create_collection();

    // Create a new record with an invalid dimension.
    let new_record = Record::random(DIMENSION + 1);

    // Assert the new record is not inserted.
    assert_eq!(collection.dimension(), DIMENSION);
    assert_eq!(collection.insert(&new_record).is_err(), true);
}

#[test]
fn insert_data_type_object() {
    let mut collection = create_collection();

    // Create a new record with a data of type HashMap.
    let vector = Vector::random(DIMENSION);
    let data = HashMap::from([("key", "value")]);
    let new_record = Record::new(&vector, &data.clone().into());

    collection.insert(&new_record).unwrap();

    // Assert the new data is in the collection.
    let id = VectorID::from(LEN);
    assert_eq!(collection.len(), LEN + 1);
    assert_eq!(collection.get(&id).unwrap().data, data.into());
}

#[test]
fn delete() {
    let mut collection = create_collection();

    // Delete a record from the collection.
    let id = VectorID(0);
    collection.delete(&id).unwrap();
    assert_eq!(collection.len(), LEN - 1);
}

#[test]
fn update() {
    let mut collection = create_collection();

    // New record to update.
    let id = VectorID(5);
    let record = Record::random(DIMENSION);
    collection.update(&id, &record).unwrap();

    assert_eq!(collection.len(), LEN);
    assert_eq!(collection.get(&id).unwrap().data, record.data);
}

#[test]
fn search() {
    let len = 1000;
    let config = Config::default();
    let records = Record::many_random(DIMENSION, len);
    let collection = Collection::build(&config, &records).unwrap();

    // Generate a random query vector.
    let query = Vector::random(DIMENSION);

    // Get the approximate and true nearest neighbors.
    let result = collection.search(&query, 5).unwrap();
    let truth = collection.true_search(&query, 10).unwrap();

    // Collect the distances from the true nearest neighbors.
    let distances: Vec<f32> = truth.par_iter().map(|i| i.distance).collect();

    assert_eq!(result.len(), 5);

    // The search is not always exact, so we check if
    // the distance is within the true distances.
    assert_eq!(distances.contains(&result[0].distance), true);
}

#[test]
fn get() {
    let records = Record::many_random(DIMENSION, LEN);
    let config = Config::default();
    let collection = Collection::build(&config, &records).unwrap();

    // Get a record from the collection.
    let index: usize = 5;
    let id = VectorID::from(index);
    let record = collection.get(&id).unwrap();

    assert_eq!(record.data, records[index].data);
    assert_eq!(record.vector, records[index].vector);
}

#[test]
fn list() {
    let collection = create_collection();
    let list = collection.list().unwrap();
    assert_eq!(list.len(), LEN);
    assert_eq!(list.len(), collection.len());
}
