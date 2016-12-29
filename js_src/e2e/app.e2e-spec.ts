import { WebSrcPage } from './app.po';

describe('web-src App', function() {
  let page: WebSrcPage;

  beforeEach(() => {
    page = new WebSrcPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
