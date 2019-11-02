import java.util.ArrayList;
import java.util.HashMap;

class Pair<T, T1> {
    T first;
    T1 second;
    Pair(T first, T1 second){
        this.first = first;
        this.second = second;
    }
}

public class UBT {

    public static void main(String [] args){
        ArrayList<Pair<Integer,Integer>> pairs = new ArrayList<>();

        HashMap<Integer,ArrayList<Integer>> result = new HashMap<>();
        pairs.add(new Pair<Integer, Integer>(120, 1));
        pairs.add(new Pair<Integer, Integer>(24, 2));
        pairs.add(new Pair<Integer, Integer>(24, 3));
        pairs.add(new Pair<Integer, Integer>(24, 4));
        pairs.add(new Pair<Integer, Integer>(24, 5));

        pairs.forEach(pair->{
            if (!result.containsKey(pair.first)) {
                ArrayList<Integer> temp = new ArrayList<>();
                temp.add(pair.second);
                result.put(pair.first,temp);
            }
            else {
                ArrayList<Integer> temp = result.get(pair.first);
                temp.add(pair.second);
                result.put(pair.first, temp);
            }
        });

        result.forEach((key,valueList)-> {
            System.out.println(key +" "+ valueList.toString());
        });
    }
}
