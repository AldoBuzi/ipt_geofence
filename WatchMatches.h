/*
 *
 * (C) 2021-24 - ntop.org
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 */

#ifndef _WATCH_MATCHES_H_
#define _WATCH_MATCHES_H_

#define MAX_IDLENESS       300 /* 5 minutes */
#define DEFAULT_BAN_TIME   300 /* 5 minutes */

class WatchMatches {
private:
  u_int32_t last_match, num_matches, banned_until;

public:
  WatchMatches(u_int32_t _num_matches, u_int32_t _banned_until) {
    last_match = time(NULL);

    if(_num_matches == 0)
      _num_matches = 1;
    else if(_num_matches >= 99)
      _num_matches = 99;
    
    num_matches = _num_matches, banned_until = _banned_until;
  }

  inline u_int32_t get_last_match()       { return(last_match);   }
  inline u_int32_t get_num_matches()      { return(num_matches);  }
  void             ban_until(u_int32_t t) { banned_until = t;     }
  
  inline void      inc_matches()      { num_matches++, last_match = time(NULL); }
  inline bool      ready_to_harvest(u_int32_t when) { return((banned_until < when) ? true : false); }
};

#endif /* _WATCH_MATCHES_H_ */
