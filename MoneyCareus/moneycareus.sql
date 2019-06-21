-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Хост: 127.0.0.1
-- Время создания: Май 07 2019 г., 14:27
-- Версия сервера: 5.5.25
-- Версия PHP: 5.3.13

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `moneycareus`
--

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  `Owner_ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=9 ;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`ID`, `Name`, `Owner_ID`) VALUES
(1, 'Зарплата', 0),
(2, 'Продукты', 0),
(3, 'Коммунальные услуги', 0),
(4, 'Транспорт', 0),
(7, 'Вино и шлюхи', 7),
(8, 'Машина', 13);

-- --------------------------------------------------------

--
-- Структура таблицы `families`
--

CREATE TABLE IF NOT EXISTS `families` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  `Owner_ID` int(11) NOT NULL,
  `Balance` double NOT NULL,
  `SafeMode` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=14 ;

--
-- Дамп данных таблицы `families`
--

INSERT INTO `families` (`ID`, `Name`, `Owner_ID`, `Balance`, `SafeMode`) VALUES
(4, 'Пупкины', 0, 0, 0),
(5, 'Пупкины', 0, 0, 0),
(6, 'Пупкины', 0, 0, 0),
(7, 'Садовниковы', 1, 40527, 1),
(8, 'Садовниковы', 2, 0, 0),
(13, 'Игнатовы', 7, 90200, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Amount` double NOT NULL,
  `Type` int(11) NOT NULL,
  `Family_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `Category` int(11) NOT NULL,
  `Datetime` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=17 ;

--
-- Дамп данных таблицы `transactions`
--

INSERT INTO `transactions` (`ID`, `Amount`, `Type`, `Family_ID`, `User_ID`, `Category`, `Datetime`) VALUES
(1, 120000, 1, 7, 1, 1, 1556809021),
(2, 500, 2, 7, 1, 5, 1557061409),
(3, 579, 2, 7, 1, 5, 1557061541),
(4, 15000, 2, 7, 1, 3, 1557067893),
(5, 7000, 2, 7, 1, 4, 1557067909),
(6, 21000, 2, 7, 1, 5, 1557068124),
(7, 28510, 2, 7, 1, 7, 1557082896),
(8, 79500, 1, 13, 7, 1, 1557095664),
(9, 18000, 1, 13, 7, 1, 1557095733),
(10, 500, 2, 13, 7, 2, 1557095766),
(11, 10000, 1, 13, 7, 1, 1557095802),
(12, 40000, 1, 13, 7, 1, 1557095848),
(13, 800, 2, 13, 7, 8, 1557095871),
(14, 9134, 2, 7, 8, 7, 1557098405),
(15, 150, 2, 7, 9, 2, 1557224236),
(16, 50, 2, 7, 9, 4, 1557224245);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` text NOT NULL,
  `Password` text NOT NULL,
  `Name` text NOT NULL,
  `Family_ID` int(11) NOT NULL,
  `Status` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`ID`, `Username`, `Password`, `Name`, `Family_ID`, `Status`) VALUES
(1, 'iborland', '22599226a', 'Иван Садовников', 7, 1),
(2, 'iborlandqq', '22599226a', 'Иван Садовников', 8, 1),
(7, 'alkoluks', '22599226a', 'Михаил Игнатов', 13, 1),
(8, 'bigdick', '22599226a', 'Антон Рогозин', 7, 2),
(9, '1borland', '22599226a', 'Ванька Садовников', 7, 3);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
