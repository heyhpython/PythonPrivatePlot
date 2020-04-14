namespace mtrandom {
    const static unsigned int N = 624;
    class MT_RNG {
        public: MT_RNG();
        MT_RNG(unsigned long s);
        MT_RNG(unsigned long init_key[], int key_length);
        // initializes RNG state, called by constructors
        void init_genrand(unsigned long s);
        // generates a random number on [0,0xffffffff]-interval
        unsigned long genrand_int32();
        // generates a random number on [0,1]-real-interval
        double genrand_real1();
        private:
            unsigned long mt[N];
            int mti;
    }; // class MT_RNG
}// namespace mtrandom

