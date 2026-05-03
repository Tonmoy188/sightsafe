const fs = require('fs');
const path = require('path');
const readline = require('readline');

/**
 * SightSafe – AI Accessibility Assistant
 * Interactive environment scanning system for visually impaired seniors
 */

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Store scan history
const scanHistory = [];
let scanCount = 0;

// Detection options with risk levels
const detectionOptions = [
  { item: 'Obstacle ahead', risk: 'HIGH', messages: [
    'Caution! There is an obstacle in your path. Please stop and navigate carefully around it.',
    'Warning! An object is blocking your way. Take your time and move slowly to avoid it.',
    'Alert! Something is ahead of you. Please proceed with extra care or ask for assistance.'
  ]},
  { item: 'Stairs detected', risk: 'HIGH', messages: [
    'Important! Stairs are ahead. Please use the handrail and take one step at a time.',
    'Caution! Steps detected in front of you. Hold the railing firmly and move carefully.',
    'Warning! Stairway ahead. Please be very careful and consider asking for help if needed.'
  ]},
  { item: 'Clear path', risk: 'SAFE', messages: [
    'Good news! The path ahead is clear and safe. You may proceed confidently.',
    'All clear! No obstacles detected. You can move forward safely at your own pace.',
    'Safe to proceed! The way is clear. Walk comfortably and enjoy your journey.'
  ]},
  { item: 'Person nearby', risk: 'MEDIUM', messages: [
    'Notice: Someone is nearby. Please be aware of their presence as you move.',
    'Heads up! Another person is in the area. Move carefully to avoid any collision.',
    'Attention! A person is close by. Please proceed slowly and be mindful of others.'
  ]},
  { item: 'Uneven surface', risk: 'HIGH', messages: [
    'Caution! The ground ahead is uneven. Walk slowly and carefully to maintain balance.',
    'Warning! Irregular surface detected. Please take small steps and watch your footing.',
    'Alert! The floor is not level ahead. Move very carefully to prevent tripping or falling.'
  ]}
];

// Display welcome screen
function showWelcome() {
  console.log('\n');
  console.log('════════════════════════════════════════════════════════════════');
  console.log('                                                                ');
  console.log('           🤖 SightSafe – AI Accessibility Assistant            ');
  console.log('              For Visually Impaired Seniors                     ');
  console.log('                                                                ');
  console.log('════════════════════════════════════════════════════════════════');
  console.log('\n');
  console.log('  Welcome! This system helps you navigate safely by detecting   ');
  console.log('  obstacles, stairs, and other hazards in your environment.     ');
  console.log('\n');
  console.log('  📋 Instructions:                                              ');
  console.log('     • Press ENTER to start a new scan                          ');
  console.log('     • Type "q" or "quit" to exit and see summary               ');
  console.log('\n');
  console.log('════════════════════════════════════════════════════════════════');
  console.log('\n');
}

// Perform environment scan
function performScan() {
  return new Promise((resolve) => {
    scanCount++;
    
    console.log('\n');
    console.log('════════════════════════════════════════════════════════════════');
    console.log(`                   🔍 SCAN #${scanCount} - ANALYZING                    `);
    console.log('════════════════════════════════════════════════════════════════');
    console.log('🔧 [SYSTEM] Initializing camera sensors...');
    console.log('🔧 [SYSTEM] Loading AI detection models...');
    console.log('✅ [SYSTEM] Ready to scan!\n');
    
    setTimeout(() => {
      console.log('📸 [CAMERA] Capturing environment image...');
      console.log('🧠 [AI] Processing visual data...');
      console.log('🔍 [AI] Analyzing for obstacles and hazards...\n');
      
      setTimeout(() => {
        // Randomly select detection
        const randomIndex = Math.floor(Math.random() * detectionOptions.length);
        const detection = detectionOptions[randomIndex];
        const messageIndex = Math.floor(Math.random() * detection.messages.length);
        const message = detection.messages[messageIndex];
        
        // Generate timestamp
        const timestamp = new Date().toISOString();
        const readableTime = new Date().toLocaleString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        });
        
        // Determine status emoji
        let statusEmoji;
        if (detection.risk === 'HIGH') {
          statusEmoji = '⚠️';
        } else if (detection.risk === 'MEDIUM') {
          statusEmoji = '⚡';
        } else {
          statusEmoji = '✅';
        }
        
        // Create scan record
        const scanRecord = {
          scanNumber: scanCount,
          timestamp: timestamp,
          detectedItem: detection.item,
          riskLevel: detection.risk,
          message: message
        };
        
        // Add to history
        scanHistory.push(scanRecord);
        
        // Display results
        console.log('════════════════════════════════════════════════════════════════');
        console.log('                     📊 DETECTION RESULTS                       ');
        console.log('════════════════════════════════════════════════════════════════');
        console.log('');
        console.log(`  📅 Time:            ${readableTime}`);
        console.log(`  🎯 Detected:        ${detection.item}`);
        console.log(`  ${statusEmoji} Risk Level:      ${detection.risk}`);
        console.log('');
        console.log('  💬 Safety Message:');
        console.log(`     ${message}`);
        console.log('');
        console.log('════════════════════════════════════════════════════════════════\n');
        
        // Simulate voice output
        setTimeout(() => {
          console.log('════════════════════════════════════════════════════════════════');
          console.log('                     🔊 VOICE OUTPUT SYSTEM                     ');
          console.log('════════════════════════════════════════════════════════════════');
          console.log('🎤 [VOICE] Initializing text-to-speech...');
          console.log('🎤 [VOICE] Converting message to audio...\n');
          
          setTimeout(() => {
            console.log(`🔊 Speaking: "${message}"`);
            console.log('');
            console.log('✅ [VOICE] Audio announcement complete\n');
            console.log('════════════════════════════════════════════════════════════════\n');
            
            resolve();
          }, 800);
        }, 600);
        
      }, 1500);
    }, 800);
  });
}

// Save scan history to file
function saveScanHistory() {
  const sessionsDir = path.join(__dirname, 'bob_sessions');
  
  // Ensure directory exists
  if (!fs.existsSync(sessionsDir)) {
    fs.mkdirSync(sessionsDir, { recursive: true });
  }
  
  const logFilePath = path.join(sessionsDir, 'session_log.json');
  
  // Create session data
  const sessionData = {
    sessionStartTime: scanHistory.length > 0 ? scanHistory[0].timestamp : new Date().toISOString(),
    sessionEndTime: new Date().toISOString(),
    totalScans: scanHistory.length,
    scans: scanHistory
  };
  
  try {
    fs.writeFileSync(logFilePath, JSON.stringify(sessionData, null, 2), 'utf8');
    console.log('✅ [LOGGER] Session history saved successfully');
    console.log(`📁 [LOGGER] Location: ${logFilePath}\n`);
    return true;
  } catch (error) {
    console.error('❌ [ERROR] Failed to save session history:', error.message);
    return false;
  }
}

// Display session summary
function showSummary() {
  console.log('\n');
  console.log('════════════════════════════════════════════════════════════════');
  console.log('                     📊 SESSION SUMMARY                         ');
  console.log('════════════════════════════════════════════════════════════════');
  console.log('');
  console.log(`  Total Scans Performed: ${scanHistory.length}`);
  console.log('');
  
  if (scanHistory.length > 0) {
    // Count risk levels
    const highRisk = scanHistory.filter(s => s.riskLevel === 'HIGH').length;
    const mediumRisk = scanHistory.filter(s => s.riskLevel === 'MEDIUM').length;
    const safe = scanHistory.filter(s => s.riskLevel === 'SAFE').length;
    
    console.log('  Risk Level Breakdown:');
    console.log(`     ⚠️  HIGH Risk:    ${highRisk} scan(s)`);
    console.log(`     ⚡ MEDIUM Risk:  ${mediumRisk} scan(s)`);
    console.log(`     ✅ SAFE:         ${safe} scan(s)`);
    console.log('');
    console.log('  Scan History:');
    console.log('  ────────────────────────────────────────────────────────────');
    
    scanHistory.forEach((scan, index) => {
      const time = new Date(scan.timestamp).toLocaleTimeString('en-US');
      let emoji = scan.riskLevel === 'HIGH' ? '⚠️' : scan.riskLevel === 'MEDIUM' ? '⚡' : '✅';
      console.log(`  ${index + 1}. [${time}] ${emoji} ${scan.detectedItem} (${scan.riskLevel})`);
    });
    
    console.log('  ────────────────────────────────────────────────────────────');
  } else {
    console.log('  No scans were performed in this session.');
  }
  
  console.log('');
  console.log('════════════════════════════════════════════════════════════════');
  console.log('                                                                ');
  console.log('         Thank you for using SightSafe! Stay Safe! 🛡️          ');
  console.log('                                                                ');
  console.log('════════════════════════════════════════════════════════════════');
  console.log('\n');
}

// Main interaction loop
async function mainLoop() {
  showWelcome();
  
  const promptUser = () => {
    rl.question('Press ENTER to scan (or type "q" to quit): ', async (answer) => {
      const input = answer.trim().toLowerCase();
      
      if (input === 'q' || input === 'quit') {
        console.log('\n🔄 [SYSTEM] Ending session...\n');
        
        // Save scan history
        if (scanHistory.length > 0) {
          console.log('════════════════════════════════════════════════════════════════');
          console.log('                      💾 SAVING SESSION DATA                    ');
          console.log('════════════════════════════════════════════════════════════════\n');
          saveScanHistory();
        }
        
        // Show summary
        showSummary();
        
        rl.close();
        return;
      }
      
      // Perform scan
      await performScan();
      
      // Continue loop
      promptUser();
    });
  };
  
  promptUser();
}

// Start the application
mainLoop();

// Made with Bob
