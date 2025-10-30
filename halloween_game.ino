/*
 * Halloween Ball Toss Game - ESP32
 * 
 * 4 vibration sensors detect ball impacts.
 * One sensor is randomly chosen as "good", others are "bad".
 * Sends "GOOD" or "BAD" to laptop via serial for sound playback.
 * Randomizes every 5 seconds after a hit.
 */

const int S1_PIN = 36;  // DO of sensor 1
const int S2_PIN = 39;  // DO of sensor 2
const int S3_PIN = 34;  // DO of sensor 3
const int S4_PIN = 35;  // DO of sensor 4

// If your modules are "active-LOW" (trigger = LOW), set this to true
const bool ACTIVE_LOW = false;  // change to true if needed

// State tracking for each sensor
int last1 = -1;
int last2 = -1;
int last3 = -1;
int last4 = -1;

// Debounce timing
const unsigned long DEBOUNCE_MS = 30;
unsigned long lastChange1 = 0;
unsigned long lastChange2 = 0;
unsigned long lastChange3 = 0;
unsigned long lastChange4 = 0;

// Game state
int goodSensor = 0;  // Which sensor (1-4) is currently "good"
bool gameLocked = false;  // Lock game after a hit
unsigned long lockTime = 0;
const unsigned long LOCK_DURATION_MS = 5000;  // 5 second delay between rounds

void setup() {
  Serial.begin(115200);
  pinMode(S1_PIN, INPUT);  
  pinMode(S2_PIN, INPUT);
  pinMode(S3_PIN, INPUT);
  pinMode(S4_PIN, INPUT);

  // Seed random number generator with analog noise
  randomSeed(analogRead(0));
  
  // Pick initial good sensor
  randomizeGoodSensor();
  
  Serial.println("=================================");
  Serial.println("Halloween Ball Toss Game Started!");
  Serial.println("=================================");
  Serial.println("Waiting for ball throws...\n");
}

void loop() {
  unsigned long now = millis();

  // Check if we should unlock the game
  if (gameLocked && (now - lockTime) >= LOCK_DURATION_MS) {
    gameLocked = false;
    randomizeGoodSensor();
    Serial.println("\n--- READY FOR NEXT THROW ---\n");
  }

  // If game is locked, don't process sensor hits
  if (gameLocked) {
    delay(10);
    return;
  }

  // ---- Sensor 1 ----
  int raw1 = digitalRead(S1_PIN);
  int logical1 = ACTIVE_LOW ? (raw1 == LOW) : (raw1 == HIGH);

  if (logical1 != last1 && (now - lastChange1) > DEBOUNCE_MS) {
    lastChange1 = now;
    last1 = logical1;
    if (logical1) {
      handleHit(1);
    }
  }

  // ---- Sensor 2 ----
  int raw2 = digitalRead(S2_PIN);
  int logical2 = ACTIVE_LOW ? (raw2 == LOW) : (raw2 == HIGH);

  if (logical2 != last2 && (now - lastChange2) > DEBOUNCE_MS) {
    lastChange2 = now;
    last2 = logical2;
    if (logical2) {
      handleHit(2);
    }
  }

  // ---- Sensor 3 ----
  int raw3 = digitalRead(S3_PIN);
  int logical3 = ACTIVE_LOW ? (raw3 == LOW) : (raw3 == HIGH);

  if (logical3 != last3 && (now - lastChange3) > DEBOUNCE_MS) {
    lastChange3 = now;
    last3 = logical3;
    if (logical3) {
      handleHit(3);
    }
  }

  // ---- Sensor 4 ----
  int raw4 = digitalRead(S4_PIN);
  int logical4 = ACTIVE_LOW ? (raw4 == LOW) : (raw4 == HIGH);

  if (logical4 != last4 && (now - lastChange4) > DEBOUNCE_MS) {
    lastChange4 = now;
    last4 = logical4;
    if (logical4) {
      handleHit(4);
    }
  }

  delay(10);
}

void handleHit(int sensorNumber) {
  Serial.print(">>> HIT DETECTED on Sensor ");
  Serial.println(sensorNumber);
  
  if (sensorNumber == goodSensor) {
    Serial.println("✓ CORRECT! Sending GOOD signal...");
    Serial.println("GOOD");  // This is what the laptop listens for
  } else {
    Serial.println("✗ WRONG! Sending BAD signal...");
    Serial.println("BAD");   // This is what the laptop listens for
  }
  
  // Lock the game for 5 seconds
  gameLocked = true;
  lockTime = millis();
  Serial.println("--- Game locked for 5 seconds ---");
}

void randomizeGoodSensor() {
  int oldGood = goodSensor;
  goodSensor = random(1, 5);  // Random number between 1 and 4
  
  Serial.println("---------------------------");
  Serial.print("Good sensor is now: ");
  Serial.println(goodSensor);
  Serial.println("---------------------------");
}

