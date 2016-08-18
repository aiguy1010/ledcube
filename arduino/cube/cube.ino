const int SER = 2;
const int REG_CLOCK = 3;
const int SER_CLOCK = 4;  
const int LAYER_MAP[] = {7,5,6,8}; 

const int DELAY_MS = 1;

uint16_t layerStates[] = {0,0,0,0};

uint8_t currentLayer = 0;

void lightLayer(const uint8_t layer, const uint16_t display_data){
  uint16_t corrected_data = display_data ^ 2; // Due to a hardware issue, value sent to the second column needs to be inverted.
  
  // Disable all layers
  digitalWrite(LAYER_MAP[0], HIGH);
  digitalWrite(LAYER_MAP[1], HIGH);
  digitalWrite(LAYER_MAP[2], HIGH);
  digitalWrite(LAYER_MAP[3], HIGH);
  
  // Write display data to the columns
  digitalWrite(REG_CLOCK, LOW);
  shiftOut(SER, SER_CLOCK, MSBFIRST, (corrected_data >> 8) & 0xff);
  shiftOut(SER, SER_CLOCK, MSBFIRST, corrected_data & 0xff);
  digitalWrite(REG_CLOCK, HIGH);

  // Re-Enable the selected layer
  digitalWrite(LAYER_MAP[layer], LOW);
}

void setup() {
  // Initialize Serial
  Serial.begin(115200);
  
  // Setup Pins
  pinMode(SER, OUTPUT);
  pinMode(REG_CLOCK, OUTPUT);
  pinMode(SER_CLOCK, OUTPUT);
  for(size_t l = 0; l<4; ++l){
    pinMode(LAYER_MAP[l], OUTPUT);
  }
}

void loop() {
  char inc = Serial.read(); 
  if (inc == 42){ // This is the signal that a new cube state is coming down the line.
    Serial.print('ACK'); // Ackknowledge...
    while(Serial.available() < 8) // Hang until we have all 8 bytes of the new cube state.
    {}

    // Reset the cube state from this input
    for(int l=0; l<4; ++l){
      layerStates[l]  = Serial.read();
      layerStates[l] |= Serial.read() << 8;
    }
  }
  else if (inc == 2){ // This is a poll to see if we are the LED cube...
    Serial.write("cube_4x4x4_v0.2.0");
  }
  
  // Display
  currentLayer = (currentLayer + 1) % 4;
  lightLayer(currentLayer, layerStates[currentLayer]);
  delay(DELAY_MS);
}
