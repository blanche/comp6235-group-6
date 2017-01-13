package foundationjusteatscrap;

import GNM.GNM;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.lang3.StringEscapeUtils;

public class FoundationJustEatScrap {

    public static void main(String[] args) throws InterruptedException, IOException, FileNotFoundException {
        String cityName = "";
        List<String> webLinks = new ArrayList<>();
        ArrayList<ArrayList<String>> commentsList = new ArrayList<ArrayList<String>>();
        /*cityName- citLink- restaurantLink- restaurantID- restaurantPersonalSite- restaurantName- restaurantAdress
        restAverageRating- restAverageRating- foodQualityStar- deliveryStar- serviceStar- TotalReviewCount
        indReviewDate- indReviewName- indReviewStar- comment
         */
        //Get whole site for city list
        String wholeSite = GNM.GetWebsite("https://www.just-eat.co.uk/takeaway");
        int cityStart = wholeSite.indexOf("<div class=\"linkArchitectureLinks\">");
        int cityEnd = wholeSite.indexOf("<div class=\"c-footer\">");

        wholeSite = wholeSite.substring(cityStart, cityEnd);
        //Parse to get cities
        while (wholeSite.contains("<a href=\"")) {
            int linkPos = wholeSite.indexOf("<a href=\"/") + 9;
            wholeSite = wholeSite.substring(linkPos, wholeSite.length());
            int linkEndPos = wholeSite.indexOf("\">");
            String urlExtension = wholeSite.substring(0, linkEndPos);
            //System.out.println(urlExtension);
            webLinks.add(urlExtension);//Add each url extension
        }
        System.err.println(webLinks.size());

        int startIndex = Integer.parseInt(GNM.ReadLinesIntoArrayList("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\", "startIndex.txt").get(0));
        int endIndex = Integer.parseInt(GNM.ReadLinesIntoArrayList("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\", "endIndex.txt").get(0));
        System.out.println(startIndex);
        System.out.println("XLSX Test");
        for (int p = startIndex; p < endIndex /*webLinks.size()*/; p++) {//For each city
            System.err.println(webLinks.get(p));
            String cityLink = webLinks.get(p);
            cityName = webLinks.get(p).substring(1, webLinks.get(p).indexOf("-"));
            System.err.println(cityName);
            wholeSite = GNM.GetWebsite("https://www.just-eat.co.uk/" + webLinks.get(p));
            int restaurantListStart = wholeSite.indexOf("<div class=\"restaurants\">");
            //int restaurantListEnd = wholeSite.indexOf("<div class=\"c-footer\">");//All restaurants, open closed
            int restaurantListEnd = wholeSite.indexOf("<div class=\"heading closedRestaurantsHeading o-card\"");//All restaurants, open closed
            wholeSite = wholeSite.substring(restaurantListStart, restaurantListEnd);
            String wholeSiteEscaped = StringEscapeUtils.unescapeHtml4(wholeSite);//Decode html

            int restCnt = 0;
            ArrayList<String> existingRestaurants = new ArrayList<String>();
            boolean cityFileTracker = GNM.FileExists("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\CityRestaurantTrackers", cityName + ".txt");
            if (cityFileTracker) {
                existingRestaurants = GNM.ReadLinesIntoArrayList("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\CityRestaurantTrackers", cityName + ".txt");
            }

            while (wholeSiteEscaped.contains("data-restaurant-id=\"")) {// Iterates through restaurants in the city loop
                //System.out.println(restCnt);
                restCnt++;
                //Start iteration for each restaurant
                int restaurantBegins = wholeSiteEscaped.indexOf("<div data-restaurant-id=\"");
                int restaurantEnds = wholeSiteEscaped.indexOf("<p class=\"viewMenu\">");
                String restaurantCutHTML = wholeSiteEscaped.substring(restaurantBegins, restaurantEnds);
                //Get Restaurant ID
                int restaurantIDStart = restaurantCutHTML.indexOf("<div data-restaurant-id=\"") + 25;
                int restaurantIDEnd = restaurantCutHTML.indexOf("\" class=\"restaurant \" ");
                String restaurantID = restaurantCutHTML.substring(restaurantIDStart, restaurantIDEnd);
                //Iterate
                
                Thread.sleep(100);
                if (!existingRestaurants.contains(restaurantID)) {

                    restaurantCutHTML = restaurantCutHTML.substring(restaurantIDEnd + 10, restaurantCutHTML.length());
                    //Get Restaurant Web Adress
                    int restaurantPersonalSiteStart = restaurantCutHTML.indexOf("<a href=\"");
                    int restaurantPersonalSiteEnd = restaurantCutHTML.indexOf("\" data-gtm=");
                    String restaurantPersonalSite = restaurantCutHTML.substring(restaurantPersonalSiteStart + 9, restaurantPersonalSiteEnd);
                    restaurantPersonalSite = restaurantPersonalSite.replaceAll("menu", "reviews");
                    //System.out.println(restaurantPersonalSite);
                    //Iterate
                    restaurantCutHTML = restaurantCutHTML.substring(restaurantPersonalSiteEnd + 5, restaurantCutHTML.length());
                    //Get Restaurant Name
                    int restNameStart = restaurantCutHTML.indexOf("alt=\"");
                    int restNameEnd = restaurantCutHTML.indexOf("\" width=\"");
                    String restaurantName = restaurantCutHTML.substring(restNameStart + 5, restNameEnd);
                    System.err.println(restaurantName);
                    //Iterate
                    int adressIteration = restaurantCutHTML.indexOf("<p class=\"address\"");
                    restaurantCutHTML = restaurantCutHTML.substring(adressIteration, restaurantCutHTML.length());
                    //System.out.println(restaurantCutHTML);
                    //Get Restaurant Adress
                    int restAdressStart = restaurantCutHTML.indexOf("http://schema.org/PostalAddress\">");
                    int restAdressEnd = restaurantCutHTML.indexOf("</p>");
                    String restaurantAdress = restaurantCutHTML.substring(restAdressStart + 50, restAdressEnd - 3);
                    restaurantAdress = restaurantAdress.trim();

                    //Get individual restaurant website
                    String individualRestaurantReviewsHTML = GNM.GetWebsite("https://www.just-eat.co.uk" + restaurantPersonalSite);
                    individualRestaurantReviewsHTML = StringEscapeUtils.unescapeHtml4(individualRestaurantReviewsHTML);//Decode html
                    //Iterate
                    int hasReview = -1;
                    try {
                        hasReview = individualRestaurantReviewsHTML.indexOf("class=\"c-rating__stars\"");
                    } catch (Exception Ex) {
                    }
                    if (hasReview > 0) {
                        individualRestaurantReviewsHTML = individualRestaurantReviewsHTML.substring(individualRestaurantReviewsHTML.indexOf("class=\"c-rating__stars\""), individualRestaurantReviewsHTML.length());
                        //Get Restaurant Star
                        int averageRatingStart = individualRestaurantReviewsHTML.indexOf("<span>");
                        int averageRatingEnd = individualRestaurantReviewsHTML.indexOf("</span>");
                        String restAverageRating = individualRestaurantReviewsHTML.substring(averageRatingStart + 6, averageRatingEnd);
                        //Iterate
                        individualRestaurantReviewsHTML = individualRestaurantReviewsHTML.substring(individualRestaurantReviewsHTML.indexOf("<div class=\"u-columns\">") + 2, individualRestaurantReviewsHTML.length());
                        //Get Restaurant Food Quality
                        int foodQualityStart = individualRestaurantReviewsHTML.indexOf("Food quality");
                        int foodQualityEnd = individualRestaurantReviewsHTML.indexOf("</div>");
                        String foodQualityStar = individualRestaurantReviewsHTML.substring(foodQualityStart + 13, foodQualityEnd);
                        //System.out.println(foodQualityStar);
                        //Iterate
                        individualRestaurantReviewsHTML = individualRestaurantReviewsHTML.substring(individualRestaurantReviewsHTML.indexOf("Delivery time") - 2, individualRestaurantReviewsHTML.length());
                        //Get Restaurant Delivery
                        int deliveryStart = individualRestaurantReviewsHTML.indexOf("Delivery time");
                        int deliveryEnd = individualRestaurantReviewsHTML.indexOf("</div>");
                        String deliveryStar = individualRestaurantReviewsHTML.substring(deliveryStart + 14, deliveryEnd);
                        //System.out.println(deliveryStar);
                        //Iterate
                        individualRestaurantReviewsHTML = individualRestaurantReviewsHTML.substring(individualRestaurantReviewsHTML.indexOf("Service") - 2, individualRestaurantReviewsHTML.length());
                        //Get Restaurant Service
                        int serviceStart = individualRestaurantReviewsHTML.indexOf("Service");
                        int serviceEnd = individualRestaurantReviewsHTML.indexOf("</div>");
                        String serviceStar = individualRestaurantReviewsHTML.substring(serviceStart + 8, serviceEnd);
                        //System.out.println(serviceStar);
                        //Iterate
                        individualRestaurantReviewsHTML = individualRestaurantReviewsHTML.substring(individualRestaurantReviewsHTML.indexOf("restaurantReviewsHeader"), individualRestaurantReviewsHTML.length());
                        //Get Total review count
                        int totalReviewCntStart = individualRestaurantReviewsHTML.indexOf("<h2>");
                        int totalReviewCntEnd = individualRestaurantReviewsHTML.indexOf("reviews");
                        String TotalReviewCount = individualRestaurantReviewsHTML.substring(totalReviewCntStart + 4, totalReviewCntEnd);
                        //System.out.println(TotalReviewCount);
                        //Iterate to reviews
                        individualRestaurantReviewsHTML = individualRestaurantReviewsHTML.substring(individualRestaurantReviewsHTML.indexOf("restaurantRatings"), individualRestaurantReviewsHTML.length());
                        String reviewPage = individualRestaurantReviewsHTML;

                        ArrayList<String> restaurantDetails = new ArrayList<String>();
                        restaurantDetails.add(cityName);/*Restaurant details to add to xls*/
                        restaurantDetails.add(cityLink);
                        restaurantDetails.add(restaurantID);
                        restaurantDetails.add(restaurantPersonalSite);
                        restaurantDetails.add(restaurantName);
                        restaurantDetails.add(restaurantAdress);
                        restaurantDetails.add(restAverageRating);
                        restaurantDetails.add(foodQualityStar);
                        restaurantDetails.add(deliveryStar);
                        restaurantDetails.add(serviceStar);
                        restaurantDetails.add(TotalReviewCount);

                        commentsList = GetCommentsFromRestaurant(reviewPage, restaurantDetails);/*Comments of a single restaurant*/


                        boolean xlsExists = GNM.FileExists("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\ScrappedData", cityName + ".txt");
                        if (xlsExists) {
                            GNM.AppendToCsv("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\ScrappedData", cityName + ".txt", commentsList);
                            GNM.AppendToFile("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\CityRestaurantTrackers", cityName + ".txt", restaurantID);
                        } else {
                            GNM.CreateFileWithLine("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\CityRestaurantTrackers", cityName + ".txt", restaurantID);
                            GNM.AppendToCsv("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\ScrappedData", cityName + ".txt", commentsList);
                        }
                    }
                    wholeSiteEscaped = wholeSiteEscaped.substring(wholeSiteEscaped.indexOf("\"o-btn o-btn--primary o-btn--mid\">") + 3, wholeSiteEscaped.length());
                } else {
                    System.out.println("Restaurant passed");
                    wholeSiteEscaped = wholeSiteEscaped.substring(wholeSiteEscaped.indexOf("\"o-btn o-btn--primary o-btn--mid\">") + 3, wholeSiteEscaped.length());
                }
            }
        }
    }

    public static ArrayList<ArrayList<String>> GetCommentsFromRestaurant(String reviewPage, ArrayList<String> restaurantDetails) {
        ArrayList<ArrayList<String>> commentsList = new ArrayList<ArrayList<String>>();

        int newPageLoad = 0;
        while (reviewPage.contains("<div class=\"date\">")) {//Comments Loop

            if (newPageLoad == 1) {
                newPageLoad = 0;
                reviewPage = reviewPage.substring(reviewPage.indexOf("restaurantRatings"), reviewPage.length());
            }

            int dateStart = reviewPage.indexOf("\"date\">");
            int dateEnd = reviewPage.indexOf("</div>");
            String indReviewDate = reviewPage.substring(dateStart + 7, dateEnd);
            reviewPage = reviewPage.substring(reviewPage.indexOf("</div>") + 3, reviewPage.length());

            int nameStart = reviewPage.indexOf("\"name\">");
            int nameEnd = reviewPage.indexOf("</div>");
            String indReviewName = reviewPage.substring(nameStart + 7, nameEnd);
            reviewPage = reviewPage.substring(reviewPage.indexOf("<div class=") + 3, reviewPage.length());

            int starStart = reviewPage.indexOf("alt=\"");
            int starEnd = reviewPage.indexOf("stars ");
            String indReviewStar = reviewPage.substring(starStart + 5, starEnd - 1);
            reviewPage = reviewPage.substring(starEnd + 2, reviewPage.length());
            reviewPage = reviewPage.substring(reviewPage.indexOf("</div>") + 4, reviewPage.length());

            int noCommentIndex = reviewPage.indexOf("noComment");
            int yesCommentIndex = reviewPage.indexOf("\"comments\"");
            String comment = "No Comment";

            if (noCommentIndex < yesCommentIndex || yesCommentIndex < 0) {
            } else {
                int commentEnd = reviewPage.indexOf("</div>");
                //System.out.println(reviewPage);
                comment = reviewPage.substring(yesCommentIndex + 11, commentEnd);
                //System.out.print(comment);
            }
            //Add to aList
            ArrayList<String> singleComment = new ArrayList<>();
            /*cityName- citLink- restaurantLink- restaurantID- restaurantPersonalSite- restaurantName- restaurantAdress
                    restAverageRating- foodQualityStar- deliveryStar- serviceStar- TotalReviewCount
                    indReviewDate- indReviewName- indReviewStar- comment
             */
            singleComment.add(restaurantDetails.get(0));
            singleComment.add(restaurantDetails.get(1));
            singleComment.add(restaurantDetails.get(2));
            singleComment.add(restaurantDetails.get(3));
            singleComment.add(restaurantDetails.get(4));
            singleComment.add(restaurantDetails.get(5));
            singleComment.add(restaurantDetails.get(6));
            singleComment.add(restaurantDetails.get(7));
            singleComment.add(restaurantDetails.get(8));
            singleComment.add(restaurantDetails.get(9));
            singleComment.add(restaurantDetails.get(10));
            singleComment.add(indReviewDate);
            singleComment.add(indReviewName);
            singleComment.add(indReviewStar);
            singleComment.add(comment);

            commentsList.add(singleComment);

            if (!reviewPage.contains("<div class=\"date\">") && reviewPage.contains("nextPage")) {
                int nPStart = reviewPage.indexOf("nextPage");
                reviewPage = reviewPage.substring(nPStart - 1, reviewPage.length());
                nPStart = reviewPage.indexOf("nextPage");
                int nPEnd = reviewPage.indexOf("\">");
                String nextPageUrl = reviewPage.substring(nPStart + 16, nPEnd);
                //System.err.println(nextPageUrl);
                reviewPage = GNM.GetWebsite("https://www.just-eat.co.uk" + nextPageUrl);
                reviewPage = StringEscapeUtils.unescapeHtml4(reviewPage);//Decode html
                newPageLoad = 1;
            }
            reviewPage = reviewPage.substring(reviewPage.indexOf("<li>") + 2, reviewPage.length());
        }
        return commentsList;
    }
}
