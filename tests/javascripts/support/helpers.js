const events = require('./helpers/events.js');
const domInterfaces = require('./helpers/dom_interfaces.js');
const html = require('./helpers/html.js');
const elements = require('./helpers/elements.js');
const rendering = require('./helpers/rendering.js');

exports.triggerEvent = events.triggerEvent;
exports.clickElementWithMouse = events.clickElementWithMouse;
exports.moveSelectionToRadio = events.moveSelectionToRadio;
exports.activateRadioWithSpace = events.activateRadioWithSpace;
exports.RangeMock = domInterfaces.RangeMock;
exports.SelectionMock = domInterfaces.SelectionMock;
exports.getRadioGroup = html.getRadioGroup;
exports.getRadios = html.getRadios;
exports.element = elements.element;
exports.WindowMock = rendering.WindowMock;
exports.ScreenMock = rendering.ScreenMock;
