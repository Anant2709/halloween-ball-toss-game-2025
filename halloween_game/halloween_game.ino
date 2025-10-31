/*
 * Halloween Ball Toss Game - ESP32
 * 
 * 4 vibration sensors detect ball impacts.
 * Each sensor is worth a certain number of points: 25, 50, 75, or 100.
 * Point assignments are randomized after each hit.
 * Sends point value to laptop via serial for sound playback.
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

// Game state - Point values for each sensor (index 0-3 = sensors 1-4)
int sensorPoints[4] = {25, 50, 75, 100};
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
  
  // Randomize initial point assignments
  randomizePoints();
  
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
    randomizePoints();
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
  // Get points for this sensor (sensor 1-4 -> array index 0-3)
  int points = sensorPoints[sensorNumber - 1];
  
  Serial.print(">>> HIT DETECTED on Sensor ");
  Serial.print(sensorNumber);
  Serial.print(" - Worth ");
  Serial.print(points);
  Serial.println(" points!");
  
  // Send points to laptop (format: "POINTS:value")
  Serial.print("POINTS:");
  Serial.println(points);
  
  // Lock the game for 5 seconds
  gameLocked = true;
  lockTime = millis();
  Serial.println("--- Game locked for 5 seconds ---");
}

void randomizePoints() {
  // Fisher-Yates shuffle algorithm to randomize point assignments
  for (int i = 3; i > 0; i--) {
    int j = random(0, i + 1);
    // Swap
    int temp = sensorPoints[i];
    sensorPoints[i] = sensorPoints[j];
    sensorPoints[j] = temp;
  }
  
  // Display current point assignments
  Serial.println("---------------------------");
  Serial.println("Point assignments:");
  for (int i = 0; i < 4; i++) {
    Serial.print("  Sensor ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.print(sensorPoints[i]);
    Serial.println(" points");
  }
  Serial.println("---------------------------");
}
 
 