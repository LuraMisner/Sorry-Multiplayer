import constants
from space import Space
from reserved_type import ReservedType
from occupied_type import OccupiedType
import pygame


# Orientation: Corner by green safety, going clockwise around board.
class Board:
    def __init__(self, win):
        self.window = win
        
        # Initialize the board
        self.board = []

        # The ids of spaces in the board if it were to be just one long array
        self.inorder_mapping = [0, 1, 2, 18, 34, 50, 66, 82, 98, 3, 4, 20, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                31, 47, 46, 45, 44, 43, 42, 41, 63, 79, 78, 95, 111, 127, 143, 159, 175, 191, 207,
                                223, 239, 255, 254, 253, 237, 221, 205, 189, 173, 157, 252, 251, 235, 250, 249, 248,
                                247, 246, 245, 244, 243, 242, 241, 240, 224, 208, 209, 210, 211, 212, 213, 214, 192,
                                176, 177, 160, 144, 128, 112, 96, 80, 64, 48, 32, 16]
        self.set_up_board()

    def set_up_board(self):
        """
        Lays out the board as a long grid
        """
        # Row 0
        self.board.append(Space(0, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(1, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(2, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(3, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(4, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(5, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(6, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(7, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(8, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(9, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(10, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(11, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(12, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(13, OccupiedType.NONE, ReservedType.GREEN_SLIDE))
        self.board.append(Space(14, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(15, OccupiedType.NONE, ReservedType.NONE))

        # Row 1
        self.board.append(Space(16, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(17, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(18, OccupiedType.NONE, ReservedType.GREEN_SAFETY))
        self.board.append(Space(19, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(20, OccupiedType.NONE, ReservedType.START))
        self.board.append(Space(21, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(22, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(23, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(24, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(25, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(26, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(27, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(28, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(29, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(30, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(31, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 2
        self.board.append(Space(32, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(33, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(34, OccupiedType.NONE, ReservedType.GREEN_SAFETY))
        self.board.append(Space(35, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(36, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(37, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(38, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(39, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(40, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(41, OccupiedType.NONE, ReservedType.HOME))
        self.board.append(Space(42, OccupiedType.NONE, ReservedType.RED_SAFETY))
        self.board.append(Space(43, OccupiedType.NONE, ReservedType.RED_SAFETY))
        self.board.append(Space(44, OccupiedType.NONE, ReservedType.RED_SAFETY))
        self.board.append(Space(45, OccupiedType.NONE, ReservedType.RED_SAFETY))
        self.board.append(Space(46, OccupiedType.NONE, ReservedType.RED_SAFETY))
        self.board.append(Space(47, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 3
        self.board.append(Space(48, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(49, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(50, OccupiedType.NONE, ReservedType.GREEN_SAFETY))
        self.board.append(Space(51, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(52, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(53, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(54, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(55, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(56, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(57, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(58, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(59, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(60, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(61, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(62, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(63, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 4
        self.board.append(Space(64, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(65, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(66, OccupiedType.NONE, ReservedType.GREEN_SAFETY))
        self.board.append(Space(67, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(68, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(69, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(70, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(71, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(72, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(73, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(74, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(75, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(76, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(77, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(78, OccupiedType.NONE, ReservedType.START))
        self.board.append(Space(79, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 5
        self.board.append(Space(80, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(81, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(82, OccupiedType.NONE, ReservedType.GREEN_SAFETY))
        self.board.append(Space(83, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(84, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(85, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(86, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(87, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(88, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(89, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(90, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(91, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(92, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(93, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(94, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(95, OccupiedType.NONE, ReservedType.NONE))

        # Row 6
        self.board.append(Space(96, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(97, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(98, OccupiedType.NONE, ReservedType.HOME))
        self.board.append(Space(99, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(100, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(101, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(102, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(103, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(104, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(105, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(106, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(107, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(108, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(109, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(110, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(111, OccupiedType.NONE, ReservedType.NONE))

        # Row 7
        self.board.append(Space(112, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(113, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(114, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(115, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(116, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(117, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(118, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(119, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(120, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(121, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(122, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(123, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(124, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(125, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(126, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(127, OccupiedType.NONE, ReservedType.NONE))

        # Row 8
        self.board.append(Space(128, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(129, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(130, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(131, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(132, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(133, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(134, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(135, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(136, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(137, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(138, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(139, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(140, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(141, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(142, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(143, OccupiedType.NONE, ReservedType.NONE))

        # Row 9
        self.board.append(Space(144, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(145, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(146, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(147, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(148, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(149, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(150, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(151, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(152, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(153, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(154, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(155, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(156, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(157, OccupiedType.NONE, ReservedType.HOME))
        self.board.append(Space(158, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(159, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 10
        self.board.append(Space(160, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(161, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(162, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(163, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(164, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(165, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(166, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(167, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(168, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(169, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(170, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(171, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(172, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(173, OccupiedType.NONE, ReservedType.BLUE_SAFETY))
        self.board.append(Space(174, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(175, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 11
        self.board.append(Space(176, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(177, OccupiedType.NONE, ReservedType.START))
        self.board.append(Space(178, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(179, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(180, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(181, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(182, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(183, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(184, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(185, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(186, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(187, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(188, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(189, OccupiedType.NONE, ReservedType.BLUE_SAFETY))
        self.board.append(Space(190, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(191, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 12
        self.board.append(Space(192, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(193, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(194, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(195, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(196, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(197, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(198, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(199, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(200, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(201, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(202, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(203, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(204, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(205, OccupiedType.NONE, ReservedType.BLUE_SAFETY))
        self.board.append(Space(206, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(207, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 13
        self.board.append(Space(208, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(209, OccupiedType.NONE, ReservedType.YELLOW_SAFETY))
        self.board.append(Space(210, OccupiedType.NONE, ReservedType.YELLOW_SAFETY))
        self.board.append(Space(211, OccupiedType.NONE, ReservedType.YELLOW_SAFETY))
        self.board.append(Space(212, OccupiedType.NONE, ReservedType.YELLOW_SAFETY))
        self.board.append(Space(213, OccupiedType.NONE, ReservedType.YELLOW_SAFETY))
        self.board.append(Space(214, OccupiedType.NONE, ReservedType.HOME))
        self.board.append(Space(215, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(216, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(217, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(218, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(219, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(220, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(221, OccupiedType.NONE, ReservedType.BLUE_SAFETY))
        self.board.append(Space(222, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(223, OccupiedType.NONE, ReservedType.RED_SLIDE))

        # Row 14
        self.board.append(Space(224, OccupiedType.NONE, ReservedType.YELLOW_SLIDE))
        self.board.append(Space(225, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(226, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(227, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(228, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(229, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(230, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(231, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(232, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(233, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(234, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(235, OccupiedType.NONE, ReservedType.START))
        self.board.append(Space(236, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(237, OccupiedType.NONE, ReservedType.BLUE_SAFETY))
        self.board.append(Space(238, OccupiedType.NONE, ReservedType.OUT_OF_BOUNDS))
        self.board.append(Space(239, OccupiedType.NONE, ReservedType.NONE))

        # Row 15
        self.board.append(Space(240, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(241, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(242, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(243, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(244, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(245, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(246, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(247, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(248, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(249, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(250, OccupiedType.NONE, ReservedType.NONE))
        self.board.append(Space(251, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(252, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(253, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(254, OccupiedType.NONE, ReservedType.BLUE_SLIDE))
        self.board.append(Space(255, OccupiedType.NONE, ReservedType.NONE))

    def draw_board(self):
        """
        Draws the visual of the board
        """
        for space_id, space in enumerate(self.board):
            row = space_id // 16
            col = space_id % 16
            s_type = space.get_type()

            if s_type == ReservedType.NONE:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE,  constants.WHITE, constants.BLACK)
            elif s_type == ReservedType.OUT_OF_BOUNDS:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.BACKGROUND, constants.BACKGROUND)
            elif s_type == ReservedType.GREEN_SLIDE:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.WHITE, constants.BLACK)

                # Start of the slide
                if space_id == constants.SLIDES['Green'][0][0] or space_id == constants.SLIDES['Green'][1][0]:
                    pygame.draw.rect(self.window, constants.GREEN, ((col * constants.BOARD_SQUARE) + 1,
                                                                    (row * constants.BOARD_SQUARE) + 10,
                                                                    constants.BOARD_SQUARE - 2,
                                                                    constants.BOARD_SQUARE - 20))

                    pygame.draw.polygon(self.window, constants.BLACK, [[(col * constants.BOARD_SQUARE),
                                                                        (row * constants.BOARD_SQUARE)],
                                                                       [((col + .75) * constants.BOARD_SQUARE),
                                                                        (row * constants.BOARD_SQUARE) +
                                                                        (constants.BOARD_SQUARE // 2)],
                                                                       [col * constants.BOARD_SQUARE,
                                                                        (row + 1) * constants.BOARD_SQUARE]])

                    pygame.draw.polygon(self.window, constants.GREEN, [[(col * constants.BOARD_SQUARE) + 1,
                                                                        (row * constants.BOARD_SQUARE) + 3],
                                                                       [((col + .75) * constants.BOARD_SQUARE) - 4,
                                                                        (row * constants.BOARD_SQUARE) +
                                                                        (constants.BOARD_SQUARE // 2)],
                                                                       [(col * constants.BOARD_SQUARE) + 1,
                                                                        ((row + 1) * constants.BOARD_SQUARE) - 3]])

                # Slide ends
                elif space_id == constants.SLIDES['Green'][0][1] or space_id == constants.SLIDES['Green'][1][1]:
                    pygame.draw.rect(self.window, constants.GREEN, ((col * constants.BOARD_SQUARE) + 1,
                                                                    (row * constants.BOARD_SQUARE) + 10,
                                                                    (constants.BOARD_SQUARE - 2) // 2,
                                                                    constants.BOARD_SQUARE - 20))

                    center_x = (constants.BOARD_SQUARE * col) + (constants.BOARD_SQUARE // 2)
                    center_y = (constants.BOARD_SQUARE * row) + (constants.BOARD_SQUARE // 2) + 1
                    pygame.draw.circle(self.window, constants.BLACK, (center_x, center_y),
                                       (constants.BOARD_SQUARE // 3) + 2)
                    pygame.draw.circle(self.window, constants.GREEN, (center_x, center_y), constants.BOARD_SQUARE // 3)

                else:
                    pygame.draw.rect(self.window, constants.GREEN, ((col * constants.BOARD_SQUARE) + 1,
                                                                    (row * constants.BOARD_SQUARE) + 10,
                                                                    constants.BOARD_SQUARE - 2,
                                                                    constants.BOARD_SQUARE - 20))

            elif s_type == ReservedType.RED_SLIDE:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.WHITE, constants.BLACK)

                # Start of the slide
                if space_id == constants.SLIDES['Red'][0][0] or space_id == constants.SLIDES['Red'][1][0]:
                    pygame.draw.rect(self.window, constants.RED, ((col * constants.BOARD_SQUARE) + 10,
                                                                  (row * constants.BOARD_SQUARE) + 1,
                                                                  constants.BOARD_SQUARE - 20,
                                                                  constants.BOARD_SQUARE - 2))

                    pygame.draw.polygon(self.window, constants.BLACK, [[(col * constants.BOARD_SQUARE),
                                                                        (row * constants.BOARD_SQUARE)],
                                                                       [((col + .5) * constants.BOARD_SQUARE),
                                                                        ((row + .75) * constants.BOARD_SQUARE)],
                                                                       [(col + .98) * constants.BOARD_SQUARE,
                                                                        row * constants.BOARD_SQUARE]])

                    pygame.draw.polygon(self.window, constants.RED, [[(col * constants.BOARD_SQUARE) + 3,
                                                                      (row * constants.BOARD_SQUARE) + 1],
                                                                     [((col + .5) * constants.BOARD_SQUARE),
                                                                      ((row + .75) * constants.BOARD_SQUARE) - 4],
                                                                     [(col + .98) * constants.BOARD_SQUARE - 3,
                                                                      row * constants.BOARD_SQUARE + 1]])

                # Slide ends
                elif space_id == constants.SLIDES['Red'][0][1] or space_id == constants.SLIDES['Red'][1][1]:
                    pygame.draw.rect(self.window, constants.RED, ((col * constants.BOARD_SQUARE) + 10,
                                                                  (row * constants.BOARD_SQUARE) + 1,
                                                                  constants.BOARD_SQUARE - 20,
                                                                  (constants.BOARD_SQUARE - 2) // 2))

                    center_x = (constants.BOARD_SQUARE * col) + (constants.BOARD_SQUARE // 2)
                    center_y = (constants.BOARD_SQUARE * row) + (constants.BOARD_SQUARE // 2) + 1
                    pygame.draw.circle(self.window, constants.BLACK, (center_x, center_y),
                                       (constants.BOARD_SQUARE // 3) + 2)
                    pygame.draw.circle(self.window, constants.RED, (center_x, center_y), constants.BOARD_SQUARE // 3)

                else:
                    pygame.draw.rect(self.window, constants.RED, ((col * constants.BOARD_SQUARE) + 10,
                                                                  (row * constants.BOARD_SQUARE) + 1,
                                                                  constants.BOARD_SQUARE - 20,
                                                                  constants.BOARD_SQUARE - 2))

            elif s_type == ReservedType.BLUE_SLIDE:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.WHITE, constants.BLACK)

                # Start of the slide
                if space_id == constants.SLIDES['Blue'][0][0] or space_id == constants.SLIDES['Blue'][1][0]:
                    pygame.draw.rect(self.window, constants.BLUE, ((col * constants.BOARD_SQUARE) + 1,
                                                                   (row * constants.BOARD_SQUARE) + 10,
                                                                   constants.BOARD_SQUARE - 2,
                                                                   constants.BOARD_SQUARE - 20))

                    pygame.draw.polygon(self.window, constants.BLACK, [[((col + 1) * constants.BOARD_SQUARE),
                                                                        (row * constants.BOARD_SQUARE)],
                                                                       [((col + .25) * constants.BOARD_SQUARE),
                                                                        (row * constants.BOARD_SQUARE) +
                                                                        (constants.BOARD_SQUARE // 2)],
                                                                       [(col + 1) * constants.BOARD_SQUARE,
                                                                        (row + 1) * constants.BOARD_SQUARE]])

                    pygame.draw.polygon(self.window, constants.BLUE, [[((col + 1) * constants.BOARD_SQUARE) - 2,
                                                                       (row * constants.BOARD_SQUARE) + 4],
                                                                      [((col + .25) * constants.BOARD_SQUARE) + 4,
                                                                       (row * constants.BOARD_SQUARE) +
                                                                       (constants.BOARD_SQUARE // 2)],
                                                                      [((col + 1) * constants.BOARD_SQUARE) - 2,
                                                                       ((row + 1) * constants.BOARD_SQUARE) - 4]])

                # Slide ends
                elif space_id == constants.SLIDES['Blue'][0][1] or space_id == constants.SLIDES['Blue'][1][1]:
                    pygame.draw.rect(self.window, constants.BLUE, ((col * constants.BOARD_SQUARE) +
                                                                   constants.BOARD_SQUARE // 2,
                                                                   (row * constants.BOARD_SQUARE) + 10,
                                                                   (constants.BOARD_SQUARE - 2) // 2,
                                                                   constants.BOARD_SQUARE - 20))

                    center_x = (constants.BOARD_SQUARE * col) + (constants.BOARD_SQUARE // 2)
                    center_y = (constants.BOARD_SQUARE * row) + (constants.BOARD_SQUARE // 2) + 1
                    pygame.draw.circle(self.window, constants.BLACK, (center_x, center_y),
                                       (constants.BOARD_SQUARE // 3) + 2)
                    pygame.draw.circle(self.window, constants.BLUE, (center_x, center_y), constants.BOARD_SQUARE // 3)

                else:
                    pygame.draw.rect(self.window, constants.BLUE, ((col * constants.BOARD_SQUARE) + 1,
                                                                   (row * constants.BOARD_SQUARE) + 10,
                                                                   constants.BOARD_SQUARE - 2,
                                                                   constants.BOARD_SQUARE - 20))

            elif s_type == ReservedType.YELLOW_SLIDE:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.WHITE, constants.BLACK)

                # Start of the slide
                if space_id == constants.SLIDES['Yellow'][0][0] or space_id == constants.SLIDES['Yellow'][1][0]:
                    pygame.draw.rect(self.window, constants.YELLOW, ((col * constants.BOARD_SQUARE) + 10,
                                                                     (row * constants.BOARD_SQUARE) + 1,
                                                                     constants.BOARD_SQUARE - 20,
                                                                     constants.BOARD_SQUARE - 2))

                    pygame.draw.polygon(self.window, constants.BLACK, [[(col * constants.BOARD_SQUARE),
                                                                        ((row + 1) * constants.BOARD_SQUARE)],
                                                                       [((col + .5) * constants.BOARD_SQUARE),
                                                                        ((row + .25) * constants.BOARD_SQUARE)],
                                                                       [(col + .98) * constants.BOARD_SQUARE,
                                                                        (row + 1) * constants.BOARD_SQUARE]])

                    pygame.draw.polygon(self.window, constants.YELLOW, [[(col * constants.BOARD_SQUARE) + 3,
                                                                         ((row + 1) * constants.BOARD_SQUARE) + 1],
                                                                        [((col + .5) * constants.BOARD_SQUARE),
                                                                         ((row + .25) * constants.BOARD_SQUARE) + 4],
                                                                        [(col + .98) * constants.BOARD_SQUARE - 3,
                                                                         (row + 1) * constants.BOARD_SQUARE + 1]])

                # Slide ends
                elif space_id == constants.SLIDES['Yellow'][0][1] or space_id == constants.SLIDES['Yellow'][1][1]:
                    pygame.draw.rect(self.window, constants.YELLOW, ((col * constants.BOARD_SQUARE) + 10,
                                                                     (row * constants.BOARD_SQUARE) +
                                                                     (constants.BOARD_SQUARE // 2),
                                                                     constants.BOARD_SQUARE - 20,
                                                                     (constants.BOARD_SQUARE - 2) // 2))

                    center_x = (constants.BOARD_SQUARE * col) + (constants.BOARD_SQUARE // 2)
                    center_y = (constants.BOARD_SQUARE * row) + (constants.BOARD_SQUARE // 2) + 1
                    pygame.draw.circle(self.window, constants.BLACK, (center_x, center_y),
                                       (constants.BOARD_SQUARE // 3) + 2)
                    pygame.draw.circle(self.window, constants.YELLOW, (center_x, center_y), constants.BOARD_SQUARE // 3)

                else:
                    pygame.draw.rect(self.window, constants.YELLOW, ((col * constants.BOARD_SQUARE) + 10,
                                                                     (row * constants.BOARD_SQUARE) + 1,
                                                                     constants.BOARD_SQUARE - 20,
                                                                     constants.BOARD_SQUARE - 2))

            elif s_type == ReservedType.GREEN_SAFETY:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.GREEN, constants.BLACK)

            elif s_type == ReservedType.RED_SAFETY:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.RED, constants.BLACK)

            elif s_type == ReservedType.BLUE_SAFETY:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.BLUE, constants.BLACK)

            elif s_type == ReservedType.YELLOW_SAFETY:
                self.draw_box(col * constants.BOARD_SQUARE, row * constants.BOARD_SQUARE, constants.BOARD_SQUARE,
                              constants.BOARD_SQUARE, constants.YELLOW, constants.BLACK)

            elif s_type == ReservedType.HOME:
                center_x = (constants.BOARD_SQUARE * col) + (constants.BOARD_SQUARE // 2)
                center_y = (constants.BOARD_SQUARE * row) + (constants.BOARD_SQUARE // 2)
                pygame.draw.circle(self.window, constants.BLACK, (center_x, center_y),
                                   (constants.HOME_CIRCLE // 3) + 2)

                if space_id == constants.HOMES['Green']:
                    pygame.draw.circle(self.window, constants.GREEN, (center_x, center_y), constants.HOME_CIRCLE // 3)
                elif space_id == constants.HOMES['Red']:
                    pygame.draw.circle(self.window, constants.RED, (center_x, center_y), constants.HOME_CIRCLE // 3)
                elif space_id == constants.HOMES['Blue']:
                    pygame.draw.circle(self.window, constants.BLUE, (center_x, center_y), constants.HOME_CIRCLE // 3)
                else:
                    pygame.draw.circle(self.window, constants.YELLOW, (center_x, center_y), constants.HOME_CIRCLE // 3)

        # Draw the starts after the board is done so theyre on top

        # Green start
        pygame.draw.circle(self.window, constants.GREEN, (216, 100), constants.START_CIRCLE_2 + 4)
        pygame.draw.circle(self.window, constants.BLACK, (216, 100), constants.START_CIRCLE_2)

        # Red Start
        pygame.draw.circle(self.window, constants.RED, (668, 218), constants.START_CIRCLE_2 + 4)
        pygame.draw.circle(self.window, constants.BLACK, (668, 218), constants.START_CIRCLE_2)

        # Blue Start
        pygame.draw.circle(self.window, constants.BLUE, (550, 668), constants.START_CIRCLE_2 + 4)
        pygame.draw.circle(self.window, constants.BLACK, (550, 668), constants.START_CIRCLE_2)

        # Yellow Start
        pygame.draw.circle(self.window, constants.YELLOW, (100, 550), constants.START_CIRCLE_2 + 4)
        pygame.draw.circle(self.window, constants.BLACK, (100, 550), constants.START_CIRCLE_2)

        # Board outline
        pygame.draw.line(self.window, constants.BLACK, (769, 0), (769, 769), 4)
        pygame.draw.line(self.window, constants.BLACK, (0, 769), (769, 769), 4)

    def draw_box(self, x, y, x_length, y_length, color, outline):
        """
        Draws a box on the window
        :param x: Integer, x position of top left corner
        :param y: Integer, y position of top left corner
        :param x_length: Integer, length
        :param y_length: Integer, height
        :param color: (int, int, int), color of box
        :param outline: (int, int, int), color of outline
        """

        background = pygame.Rect(x, y, x_length, y_length)
        pygame.draw.rect(self.window, outline, background)
        rect = pygame.Rect(x + 2, y + 2, x_length - 4, y_length - 4)
        pygame.draw.rect(self.window, color, rect)
