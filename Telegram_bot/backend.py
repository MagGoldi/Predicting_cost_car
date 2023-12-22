import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

from sklearn.ensemble import RandomForestRegressor

import config
main_df = pd.read_csv(config.DATA_SET_PATH)
main_df.columns = main_df.columns.str.lower()


def get_brand() -> list:
    return sorted(main_df['brand'].unique())


def get_model(brand) -> list:
    return sorted(main_df[main_df['brand'] == brand]['model'].unique())


def get_year(brand, model) -> list:
    return [
        main_df[(main_df['brand'] == brand) & (
            main_df['model'] == model)]['year'].unique().min(),
        main_df[(main_df['brand'] == brand) & (
            main_df['model'] == model)]['year'].unique().max()
    ]


def get_params(car_data: dict) -> dict:
    new_df = main_df[(main_df['brand'] == car_data['brand']) & (main_df['model'] == car_data['model']) & (main_df['year'] == car_data['year'])]
    new_car_data = {'Condition': list(new_df['condition'].unique()),
                    'Transmission': list(new_df['transmission'].unique()),
                    'Body_type': list(new_df['body_type'].unique()),
                    'Drive_type': list(new_df['drive_type'].unique()),
                    'Count_horsepower': list(new_df['count_horsepower'].unique())}
    return new_car_data


def pre_calculate_price(car_data: dict) -> dict:
    if 'condition' not in car_data:
        car_data['condition'] = 0

    if 'transmission' not in car_data:
        car_data['transmission'] = main_df[(main_df['brand'] == car_data['brand']) & (
            main_df['model'] == car_data['model'])]['transmission'].unique()[0]

    if 'body_type' not in car_data:
        car_data['body_type'] = main_df[(main_df['brand'] == car_data['brand']) & (
            main_df['model'] == car_data['model'])]['body_type'].unique()[0]

    if 'drive_type' not in car_data:
        car_data['drive_type'] = main_df[(main_df['brand'] == car_data['brand']) & (
            main_df['model'] == car_data['model'])]['drive_type'].unique()[0]

    if 'engine_type' not in car_data:
        car_data['engine_type'] = main_df[(main_df['brand'] == car_data['brand']) & (
            main_df['model'] == car_data['model'])]['engine_type'].unique()[0]

    if 'count_horsepower' not in car_data:
        car_data['count_horsepower'] = int(main_df[(main_df['brand'] == car_data['brand']) & (
            main_df['model'] == car_data['model'])]['count_horsepower'].unique().mean())

    if 'origin' not in car_data:
        american_cars = ['Chevrolet', 'Ford']
        european_cars = ['Mercedes-Benz', 'Audi', 'BMW',
                         'Volkswagen', 'Opel', 'Peugeot', 'Renault', 'Skoda']
        russian_cars = ['ВАЗ', 'ГАЗ', 'УАЗ']
        asian_cars = ['Hyundai', 'Daewoo', 'Toyota', 'Kia', 'Datsun', 'Geely', 'Haval', 'Lexus', 'Mazda',
                      'Acura', 'Nissan', 'Honda', 'Mitsubishi', 'Subaru', 'Suzuki', 'Chery']

        if car_data['brand'] in american_cars:
            car_data['origin'] = 'American'

        if car_data['brand'] in european_cars:
            car_data['origin'] = 'European'

        if car_data['brand'] in russian_cars:
            car_data['origin'] = 'Russian'

        if car_data['brand'] in asian_cars:
            car_data['origin'] = 'Asian'

    car_data['usage_intensity'] = car_data['mileage'] / \
        (2023 - car_data['year'] + 1)

    return car_data


def calculate_price(car_data: dict, ) -> int:
    pre_car_data = pre_calculate_price(car_data)

    y = main_df["price"]
    X = main_df.drop(columns=["price"])

    df_test = pd.DataFrame([pre_car_data], columns=['brand', 'model', 'year', 'condition', 'transmission',
                           'mileage', 'body_type', 'drive_type', 'count_horsepower', 'engine_type', 'usage_intensity', 'origin'])

    numeric_features_test = ['year', 'condition',
                             'mileage', 'count_horsepower', 'usage_intensity']

    categorical_features_test = [
        'brand', 'model', 'transmission', 'body_type', 'drive_type', 'engine_type', 'origin']

    column_transformer = ColumnTransformer([
        ('scaling', StandardScaler(), numeric_features_test),
        ('ohe', OneHotEncoder(handle_unknown="ignore", drop="first"), categorical_features_test)])

    X_train_scaled = pd.DataFrame(
        column_transformer.fit_transform(X).toarray())
    test_audi_scale = pd.DataFrame(
        column_transformer.transform(df_test).toarray())

    rf_best_max_depth, rf_best_min_samples_split, rf_best_n_estimators = 20, 3, 5

    rf_model = RandomForestRegressor(
        n_estimators=rf_best_n_estimators, min_samples_split=rf_best_min_samples_split, max_depth=rf_best_max_depth
    )

    rf_model.fit(X_train_scaled, y)
    y_pred_audi = rf_model.predict(test_audi_scale)

    return int(y_pred_audi)

