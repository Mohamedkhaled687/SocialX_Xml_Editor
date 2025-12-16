"""
Data Controller - Handles data operations like parsing, statistics, error checking, and JSON export.
"""

import json
import xml.etree.ElementTree as ET
from typing import Optional, Tuple, Dict, List, Any, Union


class DataController:
    """Controller for data-related operations."""

    def __init__(self, xml_data: Optional[ET.Element] = None) -> None:
        self.xml_data: Optional[ET.Element] = xml_data

    def set_xml_data(self, xml_data: Optional[ET.Element]) -> None:
        """Set the XML data root element."""
        self.xml_data = xml_data

    def parse_user_data(self) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """
        Parse user data and return statistics.
        
        Returns:
            tuple: (success: bool, stats: dict, error: str)
        """
        if self.xml_data is None:
            return False, {}, "No data loaded. Please upload and parse an XML file first."

        try:
            users = self.xml_data.findall('.//user')

            total_followers = 0
            total_followings = 0
            total_posts = 0

            for user in users:
                followers = user.find('followers')
                following = user.find('followings')
                posts = user.findall('.//post')

                if followers is not None and followers.text:
                    try:
                        follower_count = len(followers.findall('follower'))
                        total_followers += follower_count
                    except (ValueError, AttributeError):
                        pass
                if following is not None and following.text:
                    try:
                        following_count = len(followers.findall('follower'))
                        total_followings += following_count
                    except (ValueError, AttributeError):
                        pass
                total_posts += len(posts)

            # Get sample user info
            sample_user_info = {}
            if users:
                sample_user = users[0]
                user_id = sample_user.get('id', 'N/A')
                username = sample_user.find('username')
                username_text = username.text if username is not None else "N/A"
                sample_user_info = {"id": user_id, "username": username_text}

            stats = {
                "total_users": len(users),
                "total_followers": total_followers,
                "total_following": total_followings,
                "total_posts": total_posts,
                "sample_user": sample_user_info
            }

            return True, stats, None
        except Exception as e:
            return False, {}, f"Error while parsing user data: {str(e)}"

    def check_for_errors(self) -> Tuple[bool, List[str], List[str], Optional[str]]:
        """
        Check for data integrity issues.
        
        Returns:
            tuple: (success: bool, errors: list, warnings: list, error_msg: str)
        """
        if self.xml_data is None:
            return False, [], [], "No data loaded. Please upload and parse an XML file first."

        try:
            users = self.xml_data.findall('.//user')
            errors = []
            warnings = []

            # Collect all valid user IDs for validation on followers & followings
            valid_user_ids = []
            for user in users:
                user_id = user.get('id')
                if user_id is None:
                    id_elem = user.find('id')
                    if id_elem is not None:
                        user_id = id_elem.text
                if user_id:
                    valid_user_ids.append(str(user_id))

            for idx, user in enumerate(users, 1):
                # Get user ID - try different structures
                user_id = user.get('id')
                if user_id is None:
                    id_elem = user.find('id')
                    if id_elem is not None:
                        user_id = id_elem.text

                # Check for missing ID (required)
                if not user_id:
                    errors.append(f"User #{idx}: Missing user ID")
                    continue

                # Check for missing name (required)
                name_elem = user.find('name')
                if name_elem is None or not name_elem.text:
                    errors.append(f"User {user_id}: Missing name")

                # Check followers list structure
                followers_list = []
                followers_elem = user.find('followers')
                if followers_elem is not None:
                    for follower in followers_elem.findall('follower'):
                        follower_id_elem = follower.find('id')
                        if follower_id_elem is not None and follower_id_elem.text:
                            followers_list.append(follower_id_elem.text)

                # Check followings list structure
                followings_list = []
                followings_elem = user.find('followings')
                if followings_elem is not None:
                    for following in followings_elem.findall('following'):
                        following_id_elem = following.find('id')
                        if following_id_elem is not None and following_id_elem.text:
                            followings_list.append(following_id_elem.text)

                # Validate follower IDs exist in the network
                for follower_id in followers_list:
                    if str(follower_id) not in valid_user_ids:
                        warnings.append(f"User {user_id}: Follower ID {follower_id} does not exist in network")

            return True, errors, warnings, None
        except Exception as e:
            return False, [], [], f"Error checking failed: {str(e)}"

    def calculate_statistics(self) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """
        Calculate user statistics.
        
        Returns:
            tuple: (success: bool, stats: dict, error: str)
        """
        if self.xml_data is None:
            return False, {}, "No data loaded. Please upload and parse an XML file first."

        try:
            users = self.xml_data.findall('.//user')

            total_users = len(users)
            total_posts = 0
            total_followers = 0
            total_following = 0
            ages = []

            for user in users:
                posts = user.findall('.//post')
                total_posts += len(posts)

                # Count followers - handle list structure <followers><follower><id>...</id></follower></followers>
                followers_elem = user.find('followers')
                if followers_elem is not None:
                    follower_count = len(followers_elem.findall('follower'))
                    total_followers += follower_count

                # Count followings - handle list structure <followings><following><id>...</id></following></followings>
                followings_elem = user.find('followings')
                if followings_elem is not None:
                    following_count = len(followings_elem.findall('following'))
                    total_following += following_count

                following = user.find('following')
                if following is not None and following.text:
                    try:
                        total_following += int(following.text.strip())
                    except (ValueError, AttributeError):
                        pass

            avg_followers = total_followers / total_users if total_users > 0 else 0
            avg_posts = total_posts / total_users if total_users > 0 else 0

            stats = {
                "total_users": total_users,
                "total_posts": total_posts,
                "total_followers": total_followers,
                "total_following": total_following,
                "avg_followers": avg_followers,
                "avg_posts": avg_posts
            }

            return True, stats, None
        except Exception as e:
            return False, {}, f"Statistics error: {str(e)}"

    def export_to_json(self, file_path: str) -> Tuple[bool, str, Optional[str]]:
        """
        Export XML data to JSON format.
        
        Args:
            file_path: Path to save the JSON file
        Returns:
            tuple: (success: bool, message: str, error: str)
        """
        if self.xml_data is None:
            return False, "", "No data loaded. Please upload and parse an XML file first."

        try:
            users = self.xml_data.findall('.//user')

            # Convert XML to JSON structure - only id, name, posts, and followers list
            json_data = {
                "users": []
            }

            for user in users:
                # Get user ID
                user_id = user.get('id')
                if user_id is None:
                    id_elem = user.find('id')
                    if id_elem is not None:
                        user_id = id_elem.text

                if user_id is None:
                    continue

                # Get username
                name_elem = user.find('name')
                user_name = name_elem.text.strip() if name_elem is not None and name_elem.text else None

                # Build user dict with only required fields
                user_dict = {
                    "id": user_id,
                    "name": user_name,
                    "posts": [],
                    "followers": [],
                    "followings": []

                }

                # Add posts
                for post in user.findall('.//post'):
                    content_elem = post.find('body')
                    content = content_elem.text.strip() if content_elem is not None and content_elem.text else ""

                    topics = []
                    for topic_elem in post.findall('.//topics/topic'):
                        if topic_elem is not None and topic_elem.text:
                            topics.append(topic_elem.text.strip())

                    post_dict = {
                        "id": post.get('id'),
                        "content": content,
                        "topics": topics
                    }
                    user_dict["posts"].append(post_dict)

                # Add followers list - handle both XML structures
                followers_elem = user.find('followers')
                if followers_elem is not None:
                    for follower in followers_elem.findall('follower'):
                        follower_id_elem = follower.find('id')
                        if follower_id_elem is not None and follower_id_elem.text:
                            follower_id = follower_id_elem.text.strip()
                            user_dict["followers"].append(follower_id)

                followings_elem = user.find('followings')
                if followings_elem is not None:
                    for following in followings_elem.findall('following'):
                        following_id_elem = following.find('id')
                        if following_id_elem is not None and following_id_elem.text:
                            following_id = following_id_elem.text.strip()
                            user_dict["followings"].append(following_id)

                json_data["users"].append(user_dict)

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            return True, f"Successfully exported {len(users)} users to JSON. File saved: {file_path}", None
        except Exception as e:
            return False, "", f"Failed to export to JSON: {str(e)}"

    def search_in_posts(self,
                       word: Optional[str] = None,
                       topic: Optional[str] = None
                       ) -> Optional[List[str]]:
        """
        searching ability in the post for a topic or a word
        :param word: string word to search for in all posts
        :param topic: string topic to search for in all posts
        :return: List[str], posts that has the word or the topic written in them
        when error: returns None
        """
        if self.xml_data is None:
            return None
        if (word is None and topic is None) or (word is not None and topic is not None):
            return None

        result = []
        users = self.xml_data.findall('.//user')
        for user in users:
            for post_elem in user.findall('.//post'):
                if word is not None:
                     if post_elem.text:
                        ack = post_elem.find('body').text.find(word)
                        if ack > 0:
                            result.append(f"in user: {user.find('name').text.strip()}'s. found relevant post: {post_elem.find('body').text.strip()}")
                if topic is not None:
                    for topic_elem in post_elem.findall('.//topics/topic'):
                        if topic_elem is not None and topic_elem.text:
                            ack = topic_elem.text.find(topic)
                            if ack > 0:
                                result.append(f"in user: {user.find('name').text.strip()}'s. found relevant post: {post_elem.find('body').text.strip()}")

        if len(result) == 0:
            result.append("found no relevant posts in any user's posts")

        return result
