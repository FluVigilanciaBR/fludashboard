class UserInterface {
    constructor(kwargs) {
        this._year = kwargs.year;
        this._week = kwargs.week;
        this._state = kwargs.state;
        this._tableContainer = kwargs.tableContainer;
        this._weekDisplay = kwargs.weekDisplay;
        this._radTypeState = kwargs.radTypeState;
    }

    get week() {
        return parseInt(this._week.val() || 0);
    }

    get year() {
        return parseInt(this._year.val() || 0);
    }

    get state() {
        return this._state.val() || '';
    }
}