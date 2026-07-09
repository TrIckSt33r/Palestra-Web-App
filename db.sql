CREATE TABLE `users` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `surname` varchar(255),
  `username` varchar,
  `email` varchar,
  `password` varchar,
  `role_id` int,
  `created_at` timestamp
);

CREATE TABLE `roles` (
  `id` integer PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `visita_medica` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `id_user` int,
  `visit_date` datetime,
  `doc_name` varchar(255),
  `status` varchar(255),
  `price` decimal,
  `notes` text,
  `created_at` timestamp
);

CREATE TABLE `vetrina` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `descrizione` text,
  `brand` varchar(255),
  `price` dual,
  `status` bool,
  `stock` int,
  `image_url` varchar(255)
);

CREATE TABLE `acquisti` (
  `id` int PRIMARY KEY,
  `id_user` int,
  `id_prodotto` int,
  `pourchase_date` timestamp,
  `quantita` int
);

CREATE TABLE `gym_schedule` (
  `day_of_week` tinyint PRIMARY KEY,
  `open_time` time,
  `close_time` time,
  `is_closed` boolean
);

CREATE TABLE `courses` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `description` text,
  `max_capacity` int
);

CREATE TABLE `course_sessions` (
  `id` int PRIMARY KEY,
  `course_id` int,
  `trainer_id` int,
  `day_of_week` tinyint,
  `start_time` time,
  `end_time` time,
  `room` varchar(255)
);

CREATE TABLE `subscription_plans` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `price` dual,
  `max_courses` int,
  `description` text
);

CREATE TABLE `workout_plans` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `trainer_id` int,
  `name` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date,
  `notes` text,
  `created_at` timestamp DEFAULT 'now()'
);

CREATE TABLE `workout_plan_exercises` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `workout_plan_id` int,
  `day_name` varchar(20) NOT NULL,
  `tutorial_id` int,
  `sets` int NOT NULL,
  `reps` varchar(255) NOT NULL,
  `reset_time` time,
  `exercise_notes` text,
  `order_index` int NOT NULL
);

CREATE TABLE `user_subscriptions` (
  `id` int PRIMARY KEY,
  `id_user` int,
  `plan_id` int,
  `start_date` date,
  `end_date` date,
  `status` varchar(255)
);

CREATE TABLE `course_bookings` (
  `id` int PRIMARY KEY,
  `user_id` int,
  `course_session_id` int,
  `booking_date` date NOT NULL,
  `status` varchar(255) DEFAULT 'prenotato',
  `created_at` timestamp DEFAULT (now())
);

CREATE TABLE `physical_progres` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `recorded_at` date NOT NULL,
  `weight` decimal,
  `body_fat_percentage` decimal,
  `muscle_mass` decimal,
  `chest_cm` decimal,
  `waist_cm` decimal,
  `biceps_cm` decimal,
  `notes` text
);

CREATE TABLE `announcements` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `created_by` int,
  `created_at` timestamp DEFAULT 'now()',
  `expires_at` datetime
);

CREATE TABLE `equipment_tutorials` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `machine_name` varchar(255) NOT NULL,
  `target_muscle` varchar(255),
  `desciption` text,
  `video_url` varchar(255)
);

CREATE TABLE `payments` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `amount` decimal NOT NULL,
  `payment_method` varchar(255) NOT NULL,
  `item_type` varchar(255) NOT NULL,
  `item_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT 1,
  `handled_by` int,
  `paid_at` timestamp DEFAULT (now())
);

ALTER TABLE `users` ADD FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

ALTER TABLE `visita_medica` ADD FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

ALTER TABLE `acquisti` ADD FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

ALTER TABLE `acquisti` ADD FOREIGN KEY (`id_prodotto`) REFERENCES `vetrina` (`id`);

ALTER TABLE `course_sessions` ADD FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

ALTER TABLE `course_sessions` ADD FOREIGN KEY (`trainer_id`) REFERENCES `users` (`id`);

ALTER TABLE `workout_plans` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `workout_plans` ADD FOREIGN KEY (`trainer_id`) REFERENCES `users` (`id`);

ALTER TABLE `workout_plan_exercises` ADD FOREIGN KEY (`workout_plan_id`) REFERENCES `workout_plans` (`id`);

ALTER TABLE `workout_plan_exercises` ADD FOREIGN KEY (`tutorial_id`) REFERENCES `equipment_tutorials` (`id`);

ALTER TABLE `user_subscriptions` ADD FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

ALTER TABLE `user_subscriptions` ADD FOREIGN KEY (`plan_id`) REFERENCES `subscription_plans` (`id`);

ALTER TABLE `course_bookings` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `course_bookings` ADD FOREIGN KEY (`course_session_id`) REFERENCES `course_sessions` (`id`);

ALTER TABLE `physical_progres` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `announcements` ADD FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

ALTER TABLE `payments` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `payments` ADD FOREIGN KEY (`handled_by`) REFERENCES `users` (`id`);

-- Disable foreign key checks for INSERT
SET FOREIGN_KEY_CHECKS = 0;

INSERT INTO `vetrina` (`id`, `name`, `descrizione`, `brand`, `price`, `status`, `stock`)
VALUES
  (1, 'Impact whey protein milkshake', 'proteine derivate dal latte', 'Bulk Powders', CAST('30' AS dual), TRUE, 150);
INSERT INTO `acquisti` (`id`, `id_user`, `id_prodotto`, `pourchase_date`, `quantita`)
VALUES
  (1, 1, 1, '2026-06-15', 5);
INSERT INTO `subscription_plans` (`id`, `name`, `price`, `max_courses`, `description`)
VALUES
  (1, 'Base', CAST('30' AS dual), 1, '1 corso'),
  (2, 'Premium', CAST('50' AS dual), 2, '2 corsi'),
  (3, 'ELite', CAST('65' AS dual), 3, '3 corsi');
INSERT INTO `user_subscriptions` (`id`, `id_user`, `plan_id`, `start_date`, `end_date`, `status`)
VALUES
  (1, 1, 2, '2026-07-07', '2027-07-07', 'Attivo');
INSERT INTO `course_bookings` (`id`, `user_id`, `course_session_id`, `booking_date`, `status`, `created_at`)
VALUES
  (1, 1, 1, '2026-07-10', 'prenotato', NULL);
INSERT INTO `course_sessions` (`id`, `course_id`, `trainer_id`, `day_of_week`, `start_time`, `end_time`, `room`)
VALUES
  (1, 1, 2, 1, '07:00:00', '22:00:00', 'Sala 1'),
  (2, 1, 2, 2, '07:00:00', '22:00:00', 'Sala 1'),
  (3, 1, 2, 3, '07:00:00', '22:00:00', 'Sala 1'),
  (4, 1, 2, 4, '07:00:00', '22:00:00', 'Sala 1'),
  (5, 1, 2, 5, '07:00:00', '22:00:00', 'Sala 1'),
  (6, 1, 2, 6, '07:00:00', '22:00:00', 'Sala 1'),
  (7, 2, 3, 2, '17:00:00', '18:00:00', 'Sala 2'),
  (8, 2, 3, 4, '17:00:00', '18:00:00', 'Sala 2'),
  (9, 3, 3, 1, '17:00:00', '18:00:00', 'Sala 2'),
  (10, 3, 3, 5, '17:00:00', '18:00:00', 'Sala 2');
INSERT INTO `courses` (`id`, `name`, `description`, `max_capacity`)
VALUES
  (1, 'Sala Pesi', 'intera sala con attrezzi per allenamento', 35),
  (2, 'Pilates', 'corso con istruttore di pilates', 15),
  (3, 'Yoga', 'corso di yoga con istruttore per mamme single', 20);
INSERT INTO `gym_schedule` (`day_of_week`, `open_time`, `close_time`, `is_closed`)
VALUES
  (1, '07:00:00', '22:00:00', FALSE),
  (2, '07:00:00', '22:00:00', FALSE),
  (3, '07:00:00', '22:00:00', FALSE),
  (4, '07:00:00', '22:00:00', FALSE),
  (5, '07:00:00', '22:00:00', FALSE),
  (6, '09:00:00', '18:00:00', FALSE),
  (7, NULL, NULL, TRUE);
INSERT INTO `users` (`id`, `name`, `surname`, `username`, `email`, `password`, `role_id`, `created_at`)
VALUES
  (1, 'Maria', 'Ricci', 'CallMeMary', 'call_me_mary@gmail.com', 'marybattle', 1, '2026-06-07'),
  (2, 'Luca', 'Isernia', 'Cipolla69', 'NonMettIlDave@gmail.com', 'SognoIlDave', 2, '2026-06-07'),
  (3, 'Emanuel', 'Postiglione', 'maniaco86', 'maniaco89@gmail.om', 'bambinadi3anni', 2, '2026-07-07');
INSERT INTO `roles` (`id`, `name`)
VALUES
  (1, 'utente'),
  (2, 'PT'),
  (3, 'admin');
INSERT INTO `visita_medica` (`id`, `id_user`, `visit_date`, `doc_name`, `status`, `price`, `notes`, `created_at`)
VALUES
  (1, 2, '2026-06-07', 'Maurizio Mariella', 'confirmed', 30, 'il paziente ha un forte odore di cipolla', NULL);

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
