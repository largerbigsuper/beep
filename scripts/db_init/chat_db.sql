-- chat_window
CREATE TABLE `chat_window` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_message` text COLLATE utf8mb4_unicode_ci,
  `send_id` int(11) DEFAULT NULL,
  `receive_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- chat_window_detail
CREATE TABLE `chat_window_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat_window_id` int(11) DEFAULT NULL,
  `send_id` int(11) DEFAULT NULL,
  `receive_id` int(11) DEFAULT NULL,
  `content` text COLLATE utf8mb4_unicode_ci,
  `create_date` datetime DEFAULT NULL,
  `channel_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `readed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `chat_window_detail_chat_window_id_index` (`chat_window_id`),
  KEY `chat_window_detail_send_id_index` (`send_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;