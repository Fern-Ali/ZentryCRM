class Deck {
    constructor() {
        $(".card-btn").on("click", this.drawCard.bind(this));
        $(".hide-btn").on("click", this.hideCards.bind(this));
    }

    async init() {
        let res = await axios.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1');
        this.deckID = res.data.deck_id;
    }

    async drawCard() {
        let res = await axios.get(`https://deckofcardsapi.com/api/deck/${this.deckID}/draw/?count=1`);
        this.drawnCard = res.data.cards[0];
        this.cardFace = this.drawnCard.image;
        $("#addCardHere").append(`<div class="col-1 col-sm-1" ><img style="max-width:100px;" src=${this.cardFace}></div>`);

    }

    hideCards() {
        $("#addCardHere").toggle();
        if ($(".hide-btn").text() == 'Hide Cards') {
            $(".hide-btn").text("Show Cards");
        } else {
            $(".hide-btn").text("Hide Cards");
        }
    }
}

let deck = new Deck();
deck.init();


//$(".hide-btn").click(function () {
//    $("#addCardHere").toggle();
//    if ($(".hide-btn").text() == 'Hide Cards') {
//        $(".hide-btn").text("Show Cards");
//    } else {
//        $(".hide-btn").text("Hide Cards");
//    }
//});

