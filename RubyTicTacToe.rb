VERSION = "1.0.2"

class Board
    attr_accessor :board, :turn_counter, :winner
    def initialize
        @board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
        @turn_counter = 0
        @winner = 0
    end

    def print_board
        puts "   A   B   C"
        puts "1  #{@board[0][0]} | #{@board[1][0]} | #{@board[2][0]}"
        puts "   --+---+--"
        puts "2  #{@board[0][1]} | #{@board[1][1]} | #{@board[2][1]}"
        puts "   --+---+--"
        puts "3  #{@board[0][2]} | #{@board[1][2]} | #{@board[2][2]}"
    end

    def status
        for i in (0..2) do
            if @board[i][0] == @board[i][1] && @board[i][0] == @board[i][2] && @board[i][0] != " "
                return @board[i][0]
            elsif @board[0][i] == @board[1][i] && @board[0][i] == @board[2][i] && @board[0][i] != " "
                return @board[0][i]
            end
        end
        if @board[0][0] == @board[1][1] && @board[0][0] == @board[2][2] && @board[0][0] != " "
            return @board[0][0]
        elsif @board[2][0] == @board[1][1] && @board[2][0] == @board[0][2] && @board[2][0] != " "
            return @board[2][0]
        end
        if @board.count(" ") == 9
            return 'Nobody'
        end
        return false
    end


    private

    def spin_board
        new_board = [[@board[2][0],@board[2][1],@board[2][2]],[@board[1][0],@board[1][1],@board[1][2]],[@board[0][0],@board[0][1],@board[0][2]]]
        @board = new_board
    end
end


def welcome
    100.times { puts "" }
    puts "TIC-TAC-TOE v#{VERSION}"
    puts "by CSTAICH"
    puts "======================"
    $game = Array.new
end

def menu
    puts "Enter command ( new_game :: score )"
    input = gets.chomp.downcase
    case input
    when "new_game"
        $game << Board.new
        play_game
    when "score"
        x_score = 0
        o_score = 0
        $game.each do |x|
            if x.winner == 'X'; x_score += 1
            elsif x.winner == 'O'; o_score += 1
            end
        end
        puts ""
        puts "Current score is X:#{x_score} to O:#{o_score}."
        puts ""
        return
    else
        puts "unknown command"
    end
end

def play_game
    $game[-2] != nil && $game[-2].status == 'X' ? turn = 'O' : turn = 'X'
    while $game.last.status == false && $game.last.turn_counter != 9
        puts ""
        $game.last.print_board
        puts "#{turn}'s turn. Enter input in form: A1"
        input = gets.downcase.split(//)
        case input[0]
        when "a"; col = 0
        when "b"; col = 1
        when "c"; col = 2
        end
        row = input[1].to_i - 1
        if $game.last.board[col][row] == " "
            $game.last.board[col][row] = turn
            if turn == 'X'
                turn = 'O'
            else
                turn = 'X'
            end
            $game.last.turn_counter += 1
        else
            puts ""
            puts "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            puts "You can't go there, that space is taken."
            puts "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        end
    end
    if $game.last.status == false
        winner = "Nobody"
    else
        winner = $game.last.status
        $game.last.winner = winner
    end

    10.times { puts "" }
    3.times { puts "= = = = = = = = = =" }
    puts "Game Over!  #{winner} wins!"
    3.times { puts "= = = = = = = = = =" }
    3.times { puts "" }
    $game.last.print_board
    5.times { puts "" }

end


welcome
while true do
    menu
end

$game << Board.new
$game.last.print_board
$game.last.status
