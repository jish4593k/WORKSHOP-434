import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashSet;
import java.util.Set;

public class AdvancedWebCrawler {

    public static Set<String> crawlPage(String url) {
        Set<String> urls = new HashSet<>();
        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            Document doc = Jsoup.parse(response.body());
            Elements links = doc.select("a[href]");

            for (Element link : links) {
                String href = link.attr("abs:href");
                if (href.startsWith("http")) {
                    href = href.split("#")[0];
                    urls.add(href);
                }
            }
        } catch (IOException | InterruptedException e) {
            System.out.println("Crawling failed for " + url + " | Exception: " + e.getMessage());
        }
        return urls;
    }

    public static void analyzePage(String url) {
        try {
            Document doc = Jsoup.connect(url).get();
            String title = doc.title();
            System.out.println("Title of " + url + ": " + title);
        } catch (IOException e) {
            System.out.println("Page analysis failed for " + url + " | Exception: " + e.getMessage());
        }
    }

    public static Set<String> run(String seed, int limit) {
        Set<String> crawlFrontier = new HashSet<>();
        Set<String> repository = new HashSet<>();
        int count = 0;

        crawlFrontier.add(seed);

        while (!crawlFrontier.isEmpty() && count < limit) {
            String currentSeed = crawlFrontier.iterator().next();
            crawlFrontier.remove(currentSeed);

            Set<String> urls = crawlPage(currentSeed);
            urls.removeAll(repository);

            crawlFrontier.addAll(urls);
            count++;
            repository.add(currentSeed);

            analyzePage(currentSeed);
        }

        return repository;
    }

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println(" ");
            System.exit(1);
        }

        String seed = args[0];
        int limit = Integer.parseInt(args[1]);

        Set<String> urlRepo = run(seed, limit);

        for (String url : urlRepo) {
            System.out.println(url);
        }
        System.out.println("----------------------");
        System.out.println("Collected total " + urlRepo.size() + " URLs");
    }
}
