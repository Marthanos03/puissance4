<template>
  <div class="game-board">
    <!-- <PlayerForm v-if="!player1" @pseudoSaved="onPseudoSaved" /> -->
    <div class="player-form" v-if="!pseudook">
      <h2>Enter your Pseudos</h2>
      <input v-model="player1" placeholder="Player 1">
      <input v-model="player2" placeholder="Player 2">
      <button @click="savePseudo">Save</button>
    </div>
    <div v-else-if="!history">
      <div v-if="message" class="message">{{ message }}</div>
      <table>
        <tr v-for="(row, rowIndex) in board" :key="rowIndex">
          <td v-for="(cell, colIndex) in row" :key="colIndex" @click="play(colIndex)">
            <div :class="['cell', getCellClass(cell)]"></div>
          </td>
        </tr>
      </table>
      <button @click="resetGame">Reset Game</button>
      <button @click="resetPseudos">Reset Pseudos</button>
      <button @click="seeHistory">See history</button>
    </div>
    <div v-else>
      <h2>History</h2>
      <button @click="GoToGame">Go back to the game</button>
      <ul>
        <li v-for="game in games" :key="game.id">
          {{ game.winner }} won against {{ game.loser }} with {{ game.pieces }} pieces at {{ game.date_played }}.
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  },
});

export default {
  data() {
    return {
      board: [],
      currentPlayer: 1,
      message: "",
      winner: "",
      player1: "Player 1",
      player2: "Player 2",
      pieces: 0,
      pseudook: false,
      history: false,
      games: [],
    };
  },

  methods: {
    async GoToGame() {
      this.history = false;
    },
    async seeHistory() {
      try {
        const response = await apiClient.get(`/games/history`);
      this.games = response.data
      this.history = true
      } catch (error) {
          console.error(error);
        }
    },
    async savePseudo() {
        try {
          await apiClient.post(`/players/`, {
            player1: this.player1,
            player2: this.player2
        });
        this.pseudook = true
        this.message = `${this.player1}'s turn`;
        } catch (error) {
          console.error(error);
        }
    },
    async fetchGameState() {
      try {
        const response = await apiClient.get(`/game`);
        this.board = response.data.board;
        this.currentPlayer = response.data.current_player;
        this.player1 = response.data.player1;
        this.player2 = response.data.player2;
        this.winner = response.data.winner;
        this.pieces = response.data.pieces;
        if (this.winner) {
          this.message = `${this.winner} wins!`;
          this.recordGameHistory(this.winner, this.player1, this.player2, this.currentPlayer, this.pieces);
        } else {
          if (this.currentPlayer == 1) {
            this.message = `${this.player1}'s turn`;
          }
          else {
            this.message = `${this.player2}'s turn`;
          }
        }
      } catch (error) {
        console.error(error);
      }
    },
    async play(column) {
      if (this.winner) {
        this.message = `${this.winner} has already won. Please reset the game.`;
        return;
      }
      try {
        const response = await apiClient.post(`/play/${column}`);
        this.board = response.data.board;
        this.currentPlayer = response.data.current_player;
        this.player1 = response.data.player1;
        this.player2 = response.data.player2;
        this.winner = response.data.winner;
        this.pieces = response.data.pieces;
        if (this.winner) {
          this.message = `${this.winner} wins!`;
          this.recordGameHistory(this.winner, this.player1, this.player2, this.currentPlayer, this.pieces);
        } else {
          if (this.currentPlayer == 1) {
            this.message = `${this.player1}'s turn`;
          }
          else {
            this.message = `${this.player2}'s turn`;
          }        }
      } catch (error) {
        console.error(error);
      }
    },
    async resetGame() {
      try {
        const response = await apiClient.post(`/reset`);
        this.board = response.data.board;
        this.currentPlayer = response.data.current_player;
        this.player1 = response.data.player1;
        this.player2 = response.data.player2;
        this.winner = "";
        this.pieces = response.data.pieces;
        this.message = `${this.player1}'s turn`;
      } catch (error) {
        console.error(error);
      }
    },
    async resetPseudos() {
      this.resetGame()
      this.pseudook = false;
    },
    async recordGameHistory(winner, player1, player2, current_player, pieces) {
      try {
        let loser = player1;
        if (current_player == 2) {
          loser = player2
        }
        await apiClient.post(`/games/record`, {
          winner: winner,
          loser: loser,
          pieces: (pieces + 1) / 2
        });
      } catch (error) {
        console.error(error);
      }
    },
    getCellClass(cell) {
      if (cell === 1) return 'player1';
      if (cell === 2) return 'player2';
      return 'empty';
    },
    onPseudoSaved(player) {
      this.playerId = player.id;
    }
  },
  mounted() {
    this.fetchGameState();
  }
};
</script>

<style scoped>
  .game-board {
    text-align: center;
    margin-top: 20px;
  }
  table {
    margin: 0 auto;
    border-spacing: 10px;
  }
  td {
    width: 50px;
    height: 50px;
    cursor: pointer;
  }
  .cell {
    width: 100%;
    height: 100%;
    border-radius: 50%;
  }
  .cell.empty {
    background-color: #e0e0e0;
  }
  .cell.player1 {
    background-color: #f00;
  }
  .cell.player2 {
    background-color: #00f;
  }
  .message {
    font-size: 1.5em;
    margin-bottom: 20px;
  }
  button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 1em;
    cursor: pointer;
  }

  .player-form {
    text-align: center;
    margin-top: 20px;
  }
  input {
    margin-bottom: 10px;
    padding: 5px;
  }
  .pseudos {
    padding: 5px 10px;
  }
  </style>
  