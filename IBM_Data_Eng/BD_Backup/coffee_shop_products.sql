-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 30, 2023 at 04:32 AM
-- Server version: 8.0.34-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `coffee_shop_products`
--

-- --------------------------------------------------------

--
-- Table structure for table `product_info_m_view`
--

CREATE TABLE `product_info_m_view` (
  `COL 1` varchar(28) DEFAULT NULL,
  `COL 2` varchar(95) DEFAULT NULL,
  `COL 3` varchar(18) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `product_info_m_view`
--

INSERT INTO `product_info_m_view` (`COL 1`, `COL 2`, `COL 3`) VALUES
('product_name', 'description', 'product_category'),
('Brazilian - Organic', 'It\'s like Carnival in a cup. Clean and smooth.', 'Coffee beans'),
('Our Old Time Diner Blend', 'Our packed blend of beans that is reminiscent of the cup of coffee you used to get at a diner. ', 'Coffee beans'),
('Espresso Roast', 'Our house blend for a good espresso shot.', 'Coffee beans'),
('Primo Espresso Roast', 'Our premium single source of hand roasted beans.', 'Coffee beans'),
('Columbian Medium Roast', 'A smooth cup of coffee any time of day. ', 'Coffee beans'),
('Ethiopia', 'From the home of coffee.', 'Coffee beans'),
('Jamacian Coffee River', 'Ya man, it will start your day off right. ', 'Coffee beans'),
('Civet Cat', 'The most expensive coffee in the world, the cats do all the work. ', 'Coffee beans'),
('Organic Decaf Blend', 'Our blend of hand picked organic beans that have been naturally decaffinated. ', 'Coffee beans'),
('Guatemalan Sustainably Grown', 'Green beans you can roast yourself. ', 'Coffee beans'),
('Lemon Grass', 'You will think you are Thailand as you sip your cuppa. ', 'Loose Tea'),
('Peppermint', 'Cool and refreshing to help calm your nerves. ', 'Loose Tea'),
('English Breakfast', 'The traditional cup to start your day.', 'Loose Tea'),
('Earl Grey', 'A full leaf of Orange Pekoe blended with organic oil of bergamot.', 'Loose Tea'),
('Serenity Green Tea', 'Mountain grown and harvested at the optimal time. ', 'Loose Tea'),
('Traditional Blend Chai', 'A traditional blend.', 'Loose Tea'),
('Morning Sunrise Chai', 'Fair trade and organic and has a warm finish. ', 'Loose Tea'),
('Spicy Eye Opener Chai', 'A spicier blend to awaken your taste buds.', 'Loose Tea'),
('Dark chocolate', 'This drinking chocolate is smooth and creamy.', 'Packaged Chocolate'),
('Sustainably Grown Organic', 'Certified organic containing the highest quality ingredients. ', 'Packaged Chocolate'),
('Chili Mayan', 'Fragrant with spices, this is the most flavourful drinking chocolate you will find.', 'Packaged Chocolate'),
('Our Old Time Diner Blend Sm', 'An honest cup a coffee.', 'Coffee'),
('Our Old Time Diner Blend Rg', 'An honest cup a coffee.', 'Coffee'),
('Our Old Time Diner Blend Lg', 'An honest cup a coffee.', 'Coffee'),
('Brazilian Sm', 'It\'s like Carnival in a cup. Clean and smooth.', 'Coffee'),
('Brazilian Rg', 'It\'s like Carnival in a cup. Clean and smooth.', 'Coffee'),
('Brazilian Lg', 'It\'s like Carnival in a cup. Clean and smooth.', 'Coffee'),
('Columbian Medium Roast Sm', 'A smooth cup of coffee any time of day. ', 'Coffee'),
('Columbian Medium Roast Rg', 'A smooth cup of coffee any time of day. ', 'Coffee'),
('Columbian Medium Roast Lg', 'A smooth cup of coffee any time of day. ', 'Coffee'),
('Ethiopia Sm', 'A bold cup when you want that something extra.', 'Coffee'),
('Ethiopia Rg', 'A bold cup when you want that something extra.', 'Coffee'),
('Ethiopia Lg', 'A bold cup when you want that something extra.', 'Coffee'),
('Jamaican Coffee River Sm', 'Still a front runner for good premium coffee. ', 'Coffee'),
('Jamaican Coffee River Rg', 'Still a front runner for good premium coffee. ', 'Coffee'),
('Jamaican Coffee River Lg', 'Still a front runner for good premium coffee. ', 'Coffee'),
('Espresso shot', 'You will think you are in Venice when you sip this one. ', 'Coffee'),
('Latte', 'You will think you are in Venice when you sip this one. ', 'Coffee'),
('Latte Rg', 'You will think you are in Venice when you sip this one. ', 'Coffee'),
('Cappuccino', 'You will think you are in Venice when you sip this one. ', 'Coffee'),
('Cappuccino Lg', 'You will think you are in Venice when you sip this one. ', 'Coffee'),
('Lemon Grass Rg', 'You will think you are in Thailand. ', 'Tea'),
('Lemon Grass Lg', 'You will think you are in Thailand. ', 'Tea'),
('Peppermint Rg', 'A cool and refreshing cup.', 'Loose Tea'),
('Peppermint Lg', 'A cool and refreshing cup.', 'Tea'),
('Serenity Green Tea Rg', 'Feel the stress leaving your body. ', 'Tea'),
('Serenity Green Tea Lg', 'Feel the stress leaving your body. ', 'Tea'),
('English Breakfast Rg', 'The Queen\'s favourite cuppa in the morning. ', 'Tea'),
('English Breakfast Lg', 'The Queen\'s favourite cuppa in the morning. ', 'Tea'),
('Earl Grey Rg', 'Tradition in a cup.', 'Tea'),
('Earl Grey Lg', 'Tradition in a cup.', 'Tea'),
('Traditional Blend Chai Rg', 'Sit back and think of the tropical breezes.', 'Tea'),
('Traditional Blend Chai Lg', 'Sit back and think of the tropical breezes.', 'Tea'),
('Morning Sunrise Chai Rg', 'Face the morning after your yoga routine. ', 'Tea'),
('Morning Sunrise Chai Lg', 'Face the morning after your yoga routine. ', 'Tea'),
('Spicy Eye Opener Chai Rg', 'When you need your eyes opened wide.', 'Tea'),
('Spicy Eye Opener Chai Lg', 'When you need your eyes opened wide.', 'Tea'),
('Dark chocolate Rg', 'Slightly bitter, but still very rich. ', 'Drinking Chocolate'),
('Dark chocolate Lg', 'Slightly bitter, but still very rich. ', 'Drinking Chocolate'),
('Sustainably Grown Organic Rg', 'Just pure notes of spice.', 'Drinking Chocolate'),
('Sustainably Grown Organic Lg', 'Just pure notes of spice.', 'Drinking Chocolate'),
('Snow Day Hot Chocolate', 'Added marshmallows for the needed sugar rush.', 'Drinking Chocolate'),
('Carmel syrup', 'Rich carmel taste', 'Flavours'),
('Hazelnut syrup', 'Bursting with nutty flavour', 'Flavours'),
('Sugar Free Vanilla syrup', 'Our favorite', 'Flavours'),
('Pumpkin Spice Latte', 'Boo, its that time of year again', 'Coffee'),
('Pumpkin Spice Latte Lg', 'Boo, its that time of year again', 'Coffee'),
('Happy Holidays hot chocolate', 'Candy cane and hot chocolate, perfect.', 'Drinking Chocolate'),
('Hazelnut Biscotti', 'Crunch!', 'Bakery'),
('Cranberry Scone', 'Like Grandma used to make', 'Bakery'),
('Chocolate Croissant', 'Chocolate flakes', 'Bakery'),
('Ginger Scone', 'Little bit of spice', 'Bakery'),
('Almond Croissant', 'Crunch!', 'Bakery'),
('Ginger Biscotti', 'Crunch!', 'Bakery'),
('Croissant', 'Flakey and buttery', 'Bakery'),
('Chocolate Chip Biscotti', 'Crunch!', 'Bakery'),
('Oatmeal Scone', 'Grannys fav', 'Bakery'),
('Scottish Cream Scone ', 'Old time comfort', 'Bakery'),
('Jumbo Savory Scone', 'Anytime, anywhere', 'Bakery'),
('I Need My Bean! Toque', 'keep your head bean warm', 'Branded'),
('I Need My Bean! T-shirt', 'Stylish chic', 'Branded'),
('I Need My Bean! Diner mug', 'Classic', 'Branded'),
('I Need My Bean! Latte cup', 'The cup and saucer set is the perfect way to enjoy your latte at home', 'Branded'),
('Chocolate syrup', 'Bursting with chocolate flavour', 'Flavours'),
('Rio Nights', '2 shots of Ouro Brasilerio and pure cane sugar syrup', 'Coffee'),
('Ouro Brasileiro shot', 'From Rio', 'Coffee'),
('Ouro Brasileiro shot promo', 'Ouro promo', 'Coffee'),
('Ginger Scone promo', 'Little bit of spice', 'Bakery');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;