<template>
  <div class="game-container">
    <GameStats v-if="stats && !currentGame" :stats="stats"/>
    <GameLobby
        v-if="gameState === GameState.LOBBY"
        @create="create"
        @join="handleJoin"
        v-model:joinGameId="joinGameId"
    />
    <GameColorSelection
        v-if="gameState === GameState.COLOR_SELECTION"
        :game="currentGame"
        :selectedColor="selectedColor"
        @selectColor="selectColor"
        @exit="exit"
    />
    <GameScreen
        v-if="gameState === GameState.GAME"
        :game="currentGame"
        :me="me"
        @move="move"
    />
    <GameOver
        v-if="gameState === GameState.GAME_OVER"
        :winners="winners"
        :players="currentGame?.players"
        @exit="exit"
    />
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useWebSocket} from "@vueuse/core";
import {EventType} from "../enums/eventType";
import GameColorSelection from "../components/GameColorSelection.vue";
import GameLobby from "../components/GameLobby.vue";
import GameStats from "../components/GameStats.vue";
import GameScreen from "../components/GameScreen.vue";
import GameOver from "../components/GameOver.vue";
import {GameState} from "../enums/gameState.ts";

const gameState = ref(GameState.LOBBY);
const joinGameId = ref<string | null>(null);
const selectedColor = ref<string | null>(null);
const currentGame = ref(null);
const winners = ref(null);
const me = ref(null);
const stats = ref<{
  total_games: number
  successfully_clicks: number
  unsuccessfully_clicks: number
  most_used_color: string
} | null>(null);

const {send} = useWebSocket(
    `${import.meta.env.VITE_WEBSOCKET_URL}/${localStorage.token}`,
    {
      autoReconnect: {
        delay: 1000
      },
      onConnected() {
        getStats();
        getMe();
        getInformation();
      },
      onMessage(_, event) {
        const response = JSON.parse(event.data);
        if (!response.ok) {
          console.log(`Detail - ${response.detail}, result - ${response.result}`);
        }

        switch (response.event_type) {
          case EventType.CREATE: {
            join(response.result);
          }
            return;
          case EventType.JOIN: {
            if (response.result === true) {
              gameState.value = GameState.COLOR_SELECTION;
            }
          }
            return;
          case EventType.INFORMATION: {
            if (response.detail === "INFORMATION") {
              if (response.result.is_started === true) {
                gameState.value = GameState.GAME;
              } else {
                gameState.value = GameState.COLOR_SELECTION;
              }
              currentGame.value = response.result;
            } else if (response.detail === "WINNERS") {
              winners.value = response.result;
              gameState.value = GameState.GAME_OVER;
            } else if (response.detail === "STARTED") {
              getInformation();
            } else {
              console.log("Got an unknown information response");
            }
          }
            return;
          case EventType.EXIT: {
            resetGameState();
          }
            return;
          case EventType.SELECT_COLOR: {
            if (typeof response.result === "string") {
              selectedColor.value = response.result;
            }
          }
            return;
          case EventType.STATS: {
            stats.value = response.result;
          }
            return;
          case EventType.GET_ME: {
            me.value = response.result;
          }
            return;
        }
      }
    }
);

const create = () => {
  send(JSON.stringify({
    event_type: EventType.CREATE
  }));
};

const exit = () => {
  send(JSON.stringify({
    event_type: EventType.EXIT
  }));
};

const handleJoin = () => {
  if (joinGameId.value) {
    join(joinGameId.value);
  }
};

const join = (gameId: string) => {
  send(JSON.stringify({
    event_type: EventType.JOIN,
    payload: {game_id: gameId}
  }));
};

const move = (x: number, y: number) => {
  send(JSON.stringify({
    event_type: EventType.MOVE,
    payload: {x, y}
  }));
};

const selectColor = (color: string) => {
  send(JSON.stringify({
    event_type: EventType.SELECT_COLOR,
    payload: {color}
  }));
};

const getStats = () => {
  send(JSON.stringify({
    event_type: EventType.STATS
  }));
};

const getMe = () => {
  send(JSON.stringify({
    event_type: EventType.GET_ME
  }));
};

const getInformation = () => {
  send(JSON.stringify({
    event_type: EventType.INFORMATION
  }));
};

const resetGameState = () => {
  joinGameId.value = null;
  selectedColor.value = null;
  currentGame.value = null;
  winners.value = null;
  gameState.value = GameState.LOBBY;
  getStats();
};
</script>

<style scoped>
.game-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Arial", sans-serif;
}
</style>
