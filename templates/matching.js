const animals = [
  { arabic: 'أسد', english: 'Lion' },
  { arabic: 'فيل', english: 'Elephant' },
  { arabic: 'زرافة', english: 'Giraffe' },
  { arabic: 'نمر', english: 'Tiger' },
  { arabic: 'قرد', english: 'Monkey' },
  { arabic: 'بطة', english: 'Duck' },
  { arabic: 'كلب', english: 'Dog' },
  { arabic: 'قطة', english: 'Cat' },
  { arabic: 'فراشة', english: 'Butterfly' },
  { arabic: 'ثعبان', english: 'Snake' },
  { arabic: 'بقرة', english: 'Cow' },
  { arabic: 'خروف', english: 'Sheep' },
  { arabic: 'جمل', english: 'Camel' },
  { arabic: 'فأر', english: 'Mouse' },
  { arabic: 'فرخ', english: 'Chicken' },
  { arabic: 'أرنب', english: 'Rabbit' }
];

const cards = [];
let selectedCards = [];
let matchedCards = [];

function createCard(animal) {
  const card = document.createElement('div');
  card.classList.add('card');
  card.textContent = animal.arabic;
  card.dataset.animal = animal.english;
  card.addEventListener('click', () => flipCard(card));
  return card;
}

function shuffleCards() {
  animals.sort(() => Math.random() - 0.5);
  for (let i = 0; i < animals.length; i++) {
    cards.push(createCard(animals[i]));
    cards.push(createCard(animals[i]));
  }
}

function flipCard(card) {
  if (selectedCards.length < 2 && !selectedCards.includes(card) && !matchedCards.includes(card)) {
    card.classList.add('selected');
    selectedCards.push(card);

    if (selectedCards.length === 2) {
      setTimeout(checkMatch, 1000);
    }
  }
}

function checkMatch() {
  const [card1, card2] = selectedCards;
  const animal1 = card1.textContent;
  const animal2 = card2.textContent;

  const isMatch = card1.dataset.animal === card2.dataset.animal;

  card1.classList.remove('selected');
  card2.classList.remove('selected');

  if (isMatch) {
    card1.classList.add('matched');
    card2.classList.add('matched');
    matchedCards.push(card1, card2);
  }

  selectedCards = [];

  checkWin();
}

function checkWin() {
  if (matchedCards.length === cards.length) {
    setTimeout(() => {
      alert('Congratulations! You have matched all animals!');
    }, 500);
  }
}

function initializeGame() {
  const gameContainer = document.getElementById('game-container');
  shuffleCards();

  for (const card of cards) {
    gameContainer.appendChild(card);
  }
}

initializeGame();
