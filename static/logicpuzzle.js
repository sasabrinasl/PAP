function checkHouse(houseNumber, color, nationality, beverage, cigarette, pet) {
    let colorValue = document.getElementById('color' + houseNumber).value;
    let nationalityValue = document.getElementById('nationality' + houseNumber).value;
    let beverageValue = document.getElementById('beverage' + houseNumber).value;
    let cigaretteValue = document.getElementById('cigarette' + houseNumber).value;
    let petValue = document.getElementById('pet' + houseNumber).value;

    if (colorValue === color && nationalityValue === nationality && beverageValue === beverage && cigaretteValue === cigarette && petValue === pet) {
        return true;
    } else {
        alert('Something is incorrect in House #' + houseNumber + '. Try again!');
        return false;
    }
}

function checkSolution() {
    if(checkHouse(1, 'yellow', 'norwegian', 'water', 'dunhill', 'cats') &&
       checkHouse(2, 'blue', 'danish', 'tea', 'blends', 'horses') &&
       checkHouse(3, 'red', 'english', 'milk', 'pallmall', 'birds') &&
       checkHouse(4, 'green', 'german', 'coffee', 'prince', 'fish') &&
       checkHouse(5, 'white', 'swedish', 'beer', 'bluemaster', 'dogs')) {
           alert('Congrats! You did it!');
    }
}