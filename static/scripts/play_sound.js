// Function to play a sound file
// This function is to be exported and used in other scripts to play sound effects during the game
export function playSound(soundFile) {
    const audio = new Audio(soundFile);
    audio.play();
}