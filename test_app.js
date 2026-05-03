const { spawn } = require('child_process');

// Test script to demonstrate the interactive app
console.log('Starting automated test of SightSafe AI Assistant...\n');

const app = spawn('node', ['app.js']);

let step = 0;
const steps = [
  { delay: 2000, input: '\n', description: 'Performing first scan' },
  { delay: 5000, input: '\n', description: 'Performing second scan' },
  { delay: 5000, input: '\n', description: 'Performing third scan' },
  { delay: 5000, input: 'q\n', description: 'Quitting and showing summary' }
];

app.stdout.on('data', (data) => {
  process.stdout.write(data);
});

app.stderr.on('data', (data) => {
  process.stderr.write(data);
});

function executeNextStep() {
  if (step < steps.length) {
    const currentStep = steps[step];
    console.log(`\n[TEST] ${currentStep.description}...\n`);
    
    setTimeout(() => {
      app.stdin.write(currentStep.input);
      step++;
      executeNextStep();
    }, currentStep.delay);
  }
}

app.on('close', (code) => {
  console.log(`\n[TEST] Application exited with code ${code}`);
  console.log('[TEST] Test completed successfully!\n');
});

// Start the test sequence
executeNextStep();

// Made with Bob
