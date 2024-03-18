
---

# General Info and Manipulator Classes

## Description
This Python module provides two classes, `GeneralInfo` and `Manipulator`, for data preprocessing tasks using the Pandas library. These classes offer functionalities to obtain general information about a DataFrame and perform various manipulations on it.

## GeneralInfo Class
The `GeneralInfo` class contains methods to retrieve general information about a DataFrame such as head and tail, descriptive statistics, information about duplicates and null values, and processing object data types.

### Methods
- `head_and_tail()`: Displays the head and tail of the DataFrame.
- `describe_and_info()`: Provides information using the `describe()` and `info()` methods of Pandas.
- `duplicated_and_null()`: Identifies duplicated data and null values in the DataFrame.
- `object_processor()`: Processes object data types, including finding index max and min values, unique values, and value counts.
- `report_general_info()`: Executes all the above methods to provide a comprehensive report on the DataFrame.

## Manipulator Class
The `Manipulator` class inherits from the `GeneralInfo` class and extends its functionalities by including operations for data manipulation such as regex-based selection and datetime parsing.

### Methods
- `select_w_regex(only_numbers, only_strings, specific, s_parameter, value)`: Selects either strings or numbers from the DataFrame using regular expressions. Can also perform specific regex-based replacements.
- `datetime_parser(column_name, as_index, parse_and_sep)`: Parses datetime values in a specified column and optionally sets them as the index or separates them into year, month, and day columns.
- `search_string(column_name, keywords, method)`: Searches for strings containing specified keywords in a given column using the `str.contains` method.

---

Now, let's create the Turkish version:

---

# General Info ve Manipulator Sınıfları

## Açıklama
Bu Python modülü, Pandas kütüphanesini kullanarak veri ön işleme görevleri için iki sınıf sağlar: `GeneralInfo` ve `Manipulator`. Bu sınıflar, bir DataFrame hakkında genel bilgileri almak ve çeşitli manipülasyonlar yapmak için işlevsellikler sunar.

## GeneralInfo Sınıfı
`GeneralInfo` sınıfı, DataFrame hakkında genel bilgileri almak için baş ve kuyruk, açıklayıcı istatistikler, çoğaltılmış veriler ve boş değerler hakkında bilgileri alma ve nesne veri tiplerini işleme gibi yöntemler içerir.

### Yöntemler
- `head_and_tail()`: DataFrame'in başını ve kuyruğunu görüntüler.
- `describe_and_info()`: Pandas'ın `describe()` ve `info()` yöntemlerini kullanarak bilgi sağlar.
- `duplicated_and_null()`: DataFrame'deki çoğaltılmış verileri ve boş değerleri belirler.
- `object_processor()`: Nesne veri tiplerini işler, en büyük ve en küçük dizin değerlerini, benzersiz değerleri ve değer sayılarını bulur.
- `report_general_info()`: Yukarıdaki tüm yöntemleri yürüterek DataFrame hakkında kapsamlı bir rapor sağlar.

## Manipulator Sınıfı
`Manipulator` sınıfı, `GeneralInfo` sınıfından miras alır ve regex tabanlı seçim ve tarih zamanı ayrıştırma gibi veri manipülasyonları için işlevselliğini genişletir.

### Yöntemler
- `select_w_regex(only_numbers, only_strings, specific, s_parameter, value)`: DataFrame'den yalnızca dize veya sayıları seçer ve düzenli ifadeler kullanır. Belirli bir regex tabanlı değiştirme yapabilir.
- `datetime_parser(column_name, as_index, parse_and_sep)`: Belirtilen sütundaki tarih saat değerlerini ayrıştırır ve isteğe bağlı olarak bunları dizin olarak ayarlar veya yıl, ay ve gün sütunlarına ayırır.
- `search_string(column_name, keywords, method)`: Belirtilen sütunda belirtilen anahtar kelimeleri içeren dizeleri arar, `str.contains` yöntemini kullanır.

---


---


#### EDA Class

The EDA (Exploratory Data Analysis) class is designed to facilitate the initial exploration of your data. This class is equipped with various methods to perform one-by-one analysis, bivariate analysis, and plotting operations.

#### Features

1. **Desktop Finder**
   - Method: `find_system_desktop()`
   - Description: This method finds the desktop path of the system where the code is executed.

2. **One-by-One Countplots**
   - Method: `one_by_one_countplots()`
   - Description: Generates countplots for each column in the DataFrame and saves the plots on the desktop.

3. **One-by-One Histplots**
   - Method: `one_by_one_histplot()`
   - Description: Generates histogram plots for each column in the DataFrame and saves the plots on the desktop.

4. **Bivariate Analysis**
   - Method: `bivariate_analysis(x: str)`
   - Description: Performs bivariate analysis including bar plots and regression plots for correlation analysis.

5. **Correlation Analyzer**
   - Method: `corr_analyzer()`
   - Description: Analyzes correlation among numeric columns in the DataFrame and generates a correlation heatmap.

6. **General EDA Report**
   - Method: `give_eda_report(x: str)`
   - Description: Runs all the methods in the class to generate a comprehensive EDA report including countplots, histplots, bivariate analysis, and correlation analysis.

#### Usage

Instantiate the `Eda` class with your DataFrame, and then call the desired method(s) to perform exploratory data analysis.


------

#### EDA Sınıfı

EDA (Keşifsel Veri Analizi) sınıfı, verilerinizin başlangıç keşfini kolaylaştırmak için tasarlanmıştır. Bu sınıf, tek tek analiz, iki değişkenli analiz ve çizim işlemleri gerçekleştirmek için çeşitli yöntemlerle donatılmıştır.

#### Özellikler

1. **Masaüstü Bulucu**
   - Metod: `find_system_desktop()`
   - Açıklama: Bu metod, kodun çalıştığı sistemin masaüstü yolunu bulur.

2. **Tek Tek Sayım Grafikleri**
   - Metod: `one_by_one_countplots()`
   - Açıklama: DataFrame'deki her sütun için sayım grafikleri oluşturur ve grafikleri masaüstüne kaydeder.

3. **Tek Tek Histogram Grafikleri**
   - Metod: `one_by_one_histplot()`
   - Açıklama: DataFrame'deki her sütun için histogram grafikleri oluşturur ve grafikleri masaüstüne kaydeder.

4. **İki Değişkenli Analiz**
   - Metod: `bivariate_analysis(x: str)`
   - Açıklama: Korelasyon analizi için çubuk grafikler ve regresyon grafikleri de dahil olmak üzere iki değişkenli analiz yapar.

5. **Korelasyon Analizcisi**
   - Metod: `corr_analyzer()`
   - Açıklama: DataFrame'deki sayısal sütunlar arasındaki korelasyonu analiz eder ve bir korelasyon ısı haritası oluşturur.

6. **Genel EDA Raporu**
   - Metod: `give_eda_report(x: str)`
   - Açıklama: Sınıftaki tüm metodları çalıştırarak, sayım grafikleri, histogram grafikleri, iki değişkenli analiz ve korelasyon analizi içeren kapsamlı bir EDA raporu oluşturur.

#### Kullanım

`Eda` sınıfını DataFrame'inizle birlikte başlatın ve ardından keşifsel veri analizi yapmak için istenen metod(lar)ı çağırın.




